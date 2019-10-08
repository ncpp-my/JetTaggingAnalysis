#include <stdlib.h>
#include "JetTaggingAnalysis/NanoAODAnalyzer/interface/EventReader.h"

using namespace JetTaggingAnalysis;

EventReader::EventReader(TChain* t, bool mc, std::string era, bool d){
  std::cout << "EventReader::EventReader()" << std::endl;
  tree     = t;
  isMC     = mc;
  eraName  = era;

  debug    = d;

  std::cout << "EventReader::EventReader() tree->LoadTree(0)" << std::endl;
  tree->LoadTree(0);

  InitBranch(tree, "run",             run);
  InitBranch(tree, "luminosityBlock", lumiBlock);
  InitBranch(tree, "event",           event);
  InitBranch(tree, "PV_npvs",         nPVs);
  InitBranch(tree, "PV_npvsGood",     nPVsGood);
  InitBranch(tree, "genWeight",       genWeight);
  InitBranch(tree, "Pileup_nTrueInt", Pileup_nTrueInt);
  //
  InitBranch(tree, "HLT_Mu50",      HLT_Mu50);
  InitBranch(tree, "HLT_TkMu50",    HLT_TkMu50);
  //
  // https://twiki.cern.ch/twiki/bin/view/CMS/MissingETOptionalFiltersRun2#2018_data
  // https://twiki.cern.ch/twiki/bin/view/CMS/MissingETOptionalFiltersRun2#2016_data
  // https://twiki.cern.ch/twiki/bin/view/CMS/MissingETOptionalFiltersRun2#2017_data
  InitBranch(tree,"Flag_goodVertices",                       Flag_goodVertices);//2016
  InitBranch(tree,"Flag_globalSuperTightHalo2016Filter",     Flag_globalSuperTightHalo2016Filter);//2016
  InitBranch(tree,"Flag_HBHENoiseFilter",                    Flag_HBHENoiseFilter);//2016
  InitBranch(tree,"Flag_HBHENoiseIsoFilter",                 Flag_HBHENoiseIsoFilter);//2016
  InitBranch(tree,"Flag_EcalDeadCellTriggerPrimitiveFilter", Flag_EcalDeadCellTriggerPrimitiveFilter);//2016
  InitBranch(tree,"Flag_BadPFMuonFilter",                    Flag_BadPFMuonFilter);//2016
  InitBranch(tree,"Flag_eeBadScFilter",                      Flag_eeBadScFilter);//2016

  std::cout << "EventReader::EventReader() Initialize objects" << std::endl;

  bool doRoccorForMuons = true;
  readerMuons       = new RecoMuonReader("Muon",        tree, isMC, eraName, doRoccorForMuons);
  readerElectrons   = new RecoElectronReader("Electron",tree, isMC, eraName);
  readerJets        = new RecoJetReader("Jet",          tree, isMC, eraName);
  readerFatJets     = new RecoFatJetReader("FatJet",    tree, isMC, eraName);
  readerMET         = new RecoMETReader("MET",          tree, isMC, eraName);
  readerTrigObjects = new TrigObjectReader("TrigObj",   tree);
  if(isMC){
    readerGenParticles = new GenParticleReader("GenPart",   tree);
    readerMuons->SetGenParticleReader(readerGenParticles); // For Gen Matching
  }
} 
bool EventReader::LoadEventFromTTree(int e)
{
  //
  // IMPORTANT that we clear all objects from previous event
  // 
  // readerMuons->Clear();
  // readerElectrons->Clear();
  // readerJets->Clear();
  // readerFatJets->Clear();
  // readerTrigObjects->Clear();
  // readerGenParticles->Clear();

  if(debug){
    std::cout<<"Get Entry "<<e<<std::endl;
    std::cout<<tree->GetCurrentFile()->GetName()<<std::endl;
    tree->Show(e);
  }

  Long64_t loadStatus = tree->LoadTree(e);
  
  if(loadStatus<0){
    std::cout << "Error "<<loadStatus<<" getting event "<<e<<std::endl; 
    return false;
  }
  tree->GetEntry(e);
  
  if(debug) std::cout<<"Got Entry = " << e << std::endl;
  if(debug) std::cout<<"Reset EventReader"<<std::endl;

  //============================================
  //
  // Pre-selection
  //
  //============================================
  passPreselTriggers = false;
  passPreselLeptons  = false;

  //============================================
  //
  // Lepton selection
  //
  //============================================
  recoMuons.clear();
  recoElectrons.clear();

  nRecoMuons     = 0;
  nRecoElectrons = 0;
  nRecoLeptons   = 0;

  muon = nullptr;

  lepChan = undefined;
  lepSF = 1.0;
  tlv_lepton = TLorentzVector();

  passOneLepton = false;
  //============================================
  //
  // Trigger selection
  //
  //============================================
  trigObjectsMuon.clear();
  trigObjectsElectron.clear();
  lepIsTrigMatch = false;

  passTrigHLT     = false;  
  passTrigMatch   = false;  
  passTrigger     = false;
  //============================================
  //
  // Object selection for fatjets
  //
  //============================================
  std::vector< RecoFatJetPtr > recoFatJets;
  std::vector< RecoFatJetPtr > signalFatJets;
  nRecoFatJets   = 0;
  nSignalFatJets = 0;

  //============================================
  // Hadronic Top/W Candidate
  //============================================
  fatjet = nullptr;
  tlv_fatjet = TLorentzVector();
  fatjet_msoftdrop = -1.0;

  fatjet_n2b1 = -9.0;
  fatjet_n3b1 = -9.0;
  fatjet_tau1 = -9.0;
  fatjet_tau2 = -9.0;
  fatjet_tau3 = -9.0;
  fatjet_deepTag_TvsQCD = -9.0;
  fatjet_deepTag_WvsQCD = -9.0;

  passFatJetCand = false;
  //============================================
  //
  // Object selection for jets 
  //
  //============================================
  recoJets.clear();
  signalJets.clear();
  nRecoJets         = 0;
  nSignalJets       = 0;

  signalJets_PassORFatjet.size();
  signalBJets_PassORFatjet.size();
  signalLightJets_PassORFatjet.size();
  nSignalJets_PassORFatjet      = 0;
  nSignalBJets_PassORFatjet     = 0;
  nSignalLightJets_PassORFatjet = 0;

  jet0_passORFatjet  = nullptr;
  tlv_jet0_passORFatjet = TLorentzVector();
  jet0_passORFatjet_isBTag = false;
  jet0_passORFatjet_sfBTag = 1.0;

  signalJets_FailORFatjet.size();
  signalBJets_FailORFatjet.size();
  signalLightJets_FailORFatjet.size();
  nSignalJets_FailORFatjet      = 0;
  nSignalBJets_FailORFatjet     = 0;
  nSignalLightJets_FailORFatjet = 0;

  //============================================
  //
  // MET and its filters
  //
  //============================================
  MET_pt  = -9.;
  MET_phi = -9.0;
  tlv_MET = TLorentzVector();

  passMETFilters = false;
  //============================================
  //
  // Leptonic W reconstruction
  //
  //============================================
  nu_pz = 0.0;
  nu_E  = 0.0;

  tlv_nu = TLorentzVector();
  tlv_Wlep = TLorentzVector();

  return true;
}
bool EventReader::PassPreselection()
{
  if(debug) std::cout<<"Do PassPreselection()"<<std::endl;
  //
  // Must have at least one PV
  //
  if(nPVsGood < 1) return false;
  // 
  // Pass any of the single-lepton triggers
  //
  if(eraName=="2016"){
    passPreselTriggers = HLT_Mu50 || HLT_TkMu50;
  }
  if (!passPreselTriggers) return false;
  // 
  // Pass ==1 leptons multiplicity requirement
  //
  readerMuons->GetRecoMuonsFromNano();
  readerElectrons->GetRecoElectronsFromNano();
  recoMuons      = readerMuons->SelectRecoMuons(muonPtMin,muonEtaMax,muonID,muonISO);
  recoElectrons  = readerElectrons->SelectRecoElectrons(elecPtMin,elecEtaMax,elecID);

  nRecoMuons     = recoMuons.size();
  nRecoElectrons = recoElectrons.size();
  nRecoLeptons   = nRecoMuons+nRecoElectrons;

  passPreselLeptons = (nRecoLeptons == 1);
  if (!passPreselLeptons) return false;

  if(debug) std::cout<<"Done PassPreselection()"<<std::endl;
  return true;
}
bool EventReader::ConstructEventHypothesis()
{
  if(debug) std::cout<<"Do ConstructEventHypothesis()"<<std::endl;
  //################################################
  //
  // Lepton selection
  //
  //#################################################
  if(debug) std::cout<<"Do One Lepton Selection"<<std::endl;

  //
  // Trigger match the leptons
  //
  readerTrigObjects->GetTrigObjectsFromNano();
  trigObjectsMuon      = readerTrigObjects->SelectTrigObjects(0.0, 1e6, TrigObjectID::Muon);
  trigObjectsElectron  = readerTrigObjects->SelectTrigObjects(0.0, 1e6, TrigObjectID::Electron);  
  HelperFunctions::MatchTrigObjectsMuon(recoMuons,trigObjectsMuon,trigMatchDR);
  HelperFunctions::MatchTrigObjectsElectron(recoElectrons,trigObjectsElectron,trigMatchDR);
  
  if(debug) std::cout<<"Check number of leptons"<<std::endl;

  //
  // FIKRI:NOTE: At this moment, lets just do muon-channel 
  // only.
  //
  if (nRecoMuons == 1){
    if(debug) std::cout<<"Exactly 1 muon"<<std::endl;
    muon = recoMuons.at(0);
    tlv_lepton = muon->p4;
    lepSF = muon->SF_MediumID;
    lepChan = muChan;
    //
    // Apply some cuts
    //
    passOneLepton = true;
    passOneLepton = tlv_lepton.Pt() > 55.;
  }
  else{
    lepChan = undefined;
    passOneLepton = false;
  }

  // Stop Event hypothesis construction if doesn't pass 
  // the following selections and also skip the event
  if(!passOneLepton) return false; 
  if(debug) std::cout<<"Done One Lepton Selection"<<std::endl;

  //################################################
  //
  // Trigger
  //
  //#################################################
  if(debug) std::cout<<"Do Trigger"<<std::endl;

  if(eraName=="2016"){
    passTrigHLT = HLT_Mu50 || HLT_TkMu50;
    if(debug && passTrigHLT) std::cout<<"2016::pass HLT mu"<<std::endl;
  }
  //
  // Check if lepton istrigger matched. 
  //
  if(muon){
    if(muon->isTrigMatch) lepIsTrigMatch = true;
  }
  if(lepIsTrigMatch) passTrigMatch = true;
  //
  // passTrigger is true only if fire HLT and any of the lepton is trig match
  //
  passTrigger = passTrigHLT && passTrigMatch;

  if(!passTrigger) return false;
  if(debug) std::cout<<"Done Trigger"<<std::endl;

  //##############################################################
  //
  // Select jets and fatjets. 
  //
  //##############################################################
  if(debug) std::cout<<"Do RecoJets & RecoFatJets Selection"<<std::endl;

  readerFatJets->GetRecoFatJetsFromNano();
  readerJets->GetRecoJetsFromNano();

  //##############################################################
  // Large-R jets
  //##############################################################
  //
  // Get all fatjets from NanoAOD
  //
  recoFatJets  = readerFatJets->SelectRecoFatJets(0.0, 10.0);
  nRecoFatJets = recoFatJets.size();

  //
  // Apply selection on fatjets
  //
  for (unsigned int i = 0; i < nRecoFatJets; i++)
  {
    RecoFatJetPtr fatjet = recoFatJets.at(i);
    // Skip jet if overlap with the leptons
    if (fatjet->p4.DeltaR(tlv_lepton) < 0.8) continue;
    // Check if it is a signal jet
    bool isSignalFatJet = fatjet->pt > fatjetPtMin && fabs(fatjet->eta) >= fatjetEtaMin && fabs(fatjet->eta) < fatjetEtaMax;
    //
    if(isSignalFatJet) signalFatJets.push_back(fatjet);
  }
  nSignalFatJets = signalFatJets.size();

  if(nSignalFatJets >= 1) passFatJetCand = true;
  if(!passFatJetCand) return false;
  //##############################################################
  // Hadronic Top/W Candidate
  //##############################################################
  //
  // Take the leading signal fatjet as the candidate
  //
  if(nSignalFatJets >= 1){
    fatjet = signalFatJets.at(0);
    tlv_fatjet = fatjet->p4;
    fatjet_msoftdrop = fatjet->msoftdrop;
    fatjet_n2b1 = fatjet->n2b1;
    fatjet_n3b1 = fatjet->n3b1;
    fatjet_tau1 = fatjet->tau1;
    fatjet_tau2 = fatjet->tau2;
    fatjet_tau3 = fatjet->tau3;
    fatjet_deepTag_TvsQCD = fatjet->deepTag_TvsQCD;
    fatjet_deepTag_WvsQCD = fatjet->deepTag_WvsQCD;
  }

  //##############################################################
  // Small-R jets
  //##############################################################
  //
  // Get all jets from NanoAOD
  //
  recoJets = readerJets->SelectRecoJets(0.0, 10.0, false);
  nRecoJets = recoJets.size();
  //
  // Apply selection on jets
  //
  for (unsigned int i = 0; i < nRecoJets; i++)
  {
    RecoJetPtr jet = recoJets.at(i);
    // Skip jet if overlap with the lepton
    if (jet->p4.DeltaR(tlv_lepton) < 0.4) continue;
    // Check if it is central jet
    bool isSignalJet = jet->pt > centralJetPtMin && fabs(jet->eta) >= centralJetEtaMin && fabs(jet->eta) < centralJetEtaMax;
    //
    if(isSignalJet) {
      signalJets.push_back(jet);
      // BTag jets
      bool isBTag = jet->CSVv2 > centralJetCSVv2Cut;
      //
      bool signalJetPassOR = jet->p4.DeltaR(tlv_fatjet) < 1.0;
      if(signalJetPassOR){
        signalJets_PassORFatjet.push_back(jet);
        if(isBTag) signalBJets_PassORFatjet.push_back(jet);
        else signalLightJets_PassORFatjet.push_back(jet);
      }
      else {
        signalJets_FailORFatjet.push_back(jet);
        if(isBTag) signalBJets_FailORFatjet.push_back(jet);
        else signalLightJets_FailORFatjet.push_back(jet);
      }
    }
  }
  nSignalJets      = signalJets.size();

  nSignalJets_PassORFatjet      = signalJets_PassORFatjet.size();
  nSignalBJets_PassORFatjet     = signalBJets_PassORFatjet.size();
  nSignalLightJets_PassORFatjet = signalLightJets_PassORFatjet.size();

  nSignalJets_FailORFatjet      = signalJets_FailORFatjet.size();
  nSignalBJets_FailORFatjet     = signalBJets_FailORFatjet.size();
  nSignalLightJets_FailORFatjet = signalLightJets_FailORFatjet.size();

  if(nSignalJets_PassORFatjet >= 1){
    jet0_passORFatjet = signalJets_PassORFatjet.at(0);
    tlv_jet0_passORFatjet = jet0_passORFatjet->p4;
    jet0_passORFatjet_isBTag = jet0_passORFatjet->CSVv2 > centralJetCSVv2Cut;
  }

  if(debug) std::cout<<"Done RecoJets & RecoFatJets Selection"<<std::endl;
  //##############################################################
  //
  // Get MET variables
  //
  //##############################################################
  MET_pt  = readerMET->pt;
  MET_phi = readerMET->phi;
  tlv_MET.SetPtEtaPhiE(MET_pt, 0., MET_phi, MET_pt);
  //
  // Assume event passMETFilters
  //
  passMETFilters = true;
  if(eraName=="2016"){
    passMETFilters &= Flag_goodVertices;
    passMETFilters &= Flag_globalSuperTightHalo2016Filter;
    passMETFilters &= Flag_HBHENoiseFilter;
    passMETFilters &= Flag_HBHENoiseIsoFilter;
    passMETFilters &= Flag_EcalDeadCellTriggerPrimitiveFilter;
    passMETFilters &= Flag_BadPFMuonFilter;
    passMETFilters &= Flag_eeBadScFilter;
  }
  //##############################################################
  //
  // Leptonic W reconstruction
  //
  //##############################################################
  nu_pz = 0.0;CalculateNeutrinoPz();
  nu_E  = sqrt(tlv_MET.Px()*tlv_MET.Px() + tlv_MET.Py()*tlv_MET.Py() + nu_pz*nu_pz);
  tlv_nu.SetPxPyPzE(tlv_MET.Px(), tlv_MET.Py(), nu_pz, nu_E);

  tlv_Wlep = tlv_nu + tlv_lepton;
 
  return true;
}
float EventReader::CalculateNeutrinoPz(){
  float pz = 0.;

  float a = (80.4*80.4)-(tlv_lepton.M()*tlv_lepton.M())+2.*tlv_lepton.Px()*tlv_MET.Px()+2.*tlv_lepton.Py()*tlv_MET.Py();
  float A = 4.*((tlv_lepton.E()*tlv_lepton.E()) - (tlv_lepton.Pz()*tlv_lepton.Pz()));
  float B = -4.*a*tlv_lepton.Pz();
  float C = 4*(tlv_lepton.E()*tlv_lepton.E())*((tlv_MET.Px()*tlv_MET.Px())+(tlv_MET.Py()*tlv_MET.Py()))-(a*a);
  float D = B*B - 4*A*C;

  //If there are real solutions, use the one with lowest pz                                            
  if (D >= 0.){
    float s1 = (-B+sqrt(D)) / (2*A);
    float s2 = (-B-sqrt(D)) / (2*A);
    if (fabs(s1) < fabs(s2)){
      pz = s1;
    }
    else{ 
      pz = s2;
    }
  }
  //Otherwise, use real part                                                                           
  else{
    pz = -B/(2*A);
  }
  return pz;
}
EventReader::~EventReader(){} 




