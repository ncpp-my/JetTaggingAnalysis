#include <iostream>
#include <iomanip>
#include <cstdio>
#include <TROOT.h>
#include <boost/bind.hpp>

#include "JetTaggingAnalysis/NanoAODAnalyzer/interface/JetTaggingTreeMaker.h"

using namespace NanoAODAnalysis;
using namespace JetTaggingAnalysis;

JetTaggingTreeMaker::JetTaggingTreeMaker(TChain* _events, TChain* _runs, TChain* _lumiBlocks,  bool _isMC, bool _blind, std::string _era, bool _debug){
  if(_debug) std::cout<<"In JetTaggingTreeMaker constructor"<<std::endl;

  clock_begin = std::chrono::steady_clock::now();

  debug           = _debug;
  isMC            = _isMC;
  blind           = _blind;
  eraName         = _era;
  eventsTree      = _events;
  runsTree        = _runs;
  lumiBlocksTree  = _lumiBlocks;
  // Switch off all branches
  eventsTree->SetBranchStatus("*", 0);

  //Calculate MC weight denominator
  if(isMC){
    runsTree->SetBranchStatus("*", 0);
    runsTree->LoadTree(0);
    InitBranch(runsTree, "genEventCount", genEventCount);
    InitBranch(runsTree, "genEventSumw",  genEventSumw);
    InitBranch(runsTree, "genEventSumw2", genEventSumw2);
    for(unsigned int r = 0; r < runsTree->GetEntries(); r++){
      runsTree->GetEntry(r);
      mcEventCount += genEventCount;
      mcEventSumw  += genEventSumw;
      mcEventSumw2 += genEventSumw2;
    }
    std::cout << "mcEventCount " << mcEventCount << " | mcEventSumw " << mcEventSumw << std::endl;
  }
  //
  // brilcalc lumi -u /fb --normtag /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_PHYSICS.json -i
  // /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions16/13TeV/ReReco/Final/Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt
  //
  if(eraName == "2016"){
    _lumi = 35921.88; //ipb
  }
  //
  // brilcalc lumi -u /fb --normtag /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_PHYSICS.json -i
  // /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/ReReco/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON.txt
  //
  else if(eraName == "2017"){
    _lumi = 41529.15; //ipb
  }
  //
  // brilcalc lumi -u /fb --normtag /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_PHYSICS.json -i
  // /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_PHYSICS.json -i /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/ReReco/Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON.txt
  //
  else if(eraName == "2018"){
    _lumi = 59740.57; //ipb
  }

  eventReader = new JetTaggingAnalysis::EventReader(eventsTree, isMC, eraName, debug);
  treeEvents  = eventsTree->GetEntries();
} 
void JetTaggingTreeMaker::CreateNtupleTree(std::string fileName){
  
  std::cout << "Output File created: " << fileName << std::endl;

  ntupleFile = TFile::Open(fileName.c_str() , "RECREATE");
  
  ntupleTree = new TTree("JetTaggingTree", "JetTaggingTree");
  ntupleTree->Branch("run",               &b_run,                  "run/I");
  ntupleTree->Branch("lumiBlock",         &b_lumiBlock,            "lumiBlock/I");
  ntupleTree->Branch("event",             &b_event,                "event/l");
  ntupleTree->Branch("nPVs",              &b_nPVs,                 "nPVs/I");
  ntupleTree->Branch("nPVsGood",          &b_nPVsGood,             "nPVsGood/I");
  ntupleTree->Branch("evtWeight",         &b_evtWeight,            "evtWeight/F");
  ntupleTree->Branch("mcXS",              &b_mcXS,                 "mcXS/F");
  ntupleTree->Branch("mcKFactor",         &b_mcKFactor,            "mcKFactor/F");
  ntupleTree->Branch("mcGenWeight",       &b_mcGenWeight,          "mcGenWeight/F");
  ntupleTree->Branch("passOneLepton",     &b_passOneLepton,        "passOneLepton/O");
  ntupleTree->Branch("passTrigger",       &b_passTrigger,          "passTrigger/O");
  ntupleTree->Branch("passFatJetCand",    &b_passFatJetCand,       "passFatJetCand/O");
  ntupleTree->Branch("lep_pt",            &b_lep_pt,               "lep_pt/F");
  ntupleTree->Branch("lep_eta",           &b_lep_eta,              "lep_eta/F");
  ntupleTree->Branch("lep_phi",           &b_lep_phi,              "lep_phi/F");
  ntupleTree->Branch("lep_SF",            &b_lep_SF,               "lep_SF/F");
  ntupleTree->Branch("lep_IsTrigMatch",   &b_lep_IsTrigMatch,      "lep_IsTrigMatch/O");
  ntupleTree->Branch("fatjet_pt",         &b_fatjet_pt,            "fatjet_pt/F");
  ntupleTree->Branch("fatjet_eta",        &b_fatjet_eta,           "fatjet_eta/F");
  ntupleTree->Branch("fatjet_phi",        &b_fatjet_phi,           "fatjet_phi/F");
  ntupleTree->Branch("fatjet_m",          &b_fatjet_m,             "fatjet_m/F");
  ntupleTree->Branch("fatjet_msoftdrop",  &b_fatjet_msoftdrop,     "fatjet_msoftdrop/F");
  ntupleTree->Branch("fatjet_n2b1",       &b_fatjet_n2b1,          "fatjet_n2b1/F");
  ntupleTree->Branch("fatjet_n3b1",       &b_fatjet_n3b1,          "fatjet_n3b1/F");
  ntupleTree->Branch("fatjet_tau1",       &b_fatjet_tau1,          "fatjet_tau1/F");
  ntupleTree->Branch("fatjet_tau2",       &b_fatjet_tau2,          "fatjet_tau2/F");
  ntupleTree->Branch("fatjet_tau3",       &b_fatjet_tau3,          "fatjet_tau3/F");
  ntupleTree->Branch("fatjet_deepTag_TvsQCD", &b_fatjet_deepTag_TvsQCD,    "fatjet_deepTag_TvsQCD/F");
  ntupleTree->Branch("fatjet_deepTag_WvsQCD", &b_fatjet_deepTag_WvsQCD,    "fatjet_deepTag_WvsQCD/F");
  ntupleTree->Branch("nSignalJets_PassORFatjet",     &b_nSignalJets_PassORFatjet,       "nSignalJets_PassORFatjet/I");
  ntupleTree->Branch("nSignalBJets_PassORFatjet",    &b_nSignalBJets_PassORFatjet,      "nSignalBJets_PassORFatjet/I");
  ntupleTree->Branch("nSignalLightJets_PassORFatjet",&b_nSignalLightJets_PassORFatjet,  "nSignalLightJets_PassORFatjet/I");
  ntupleTree->Branch("nSignalJets_FailORFatjet",     &b_nSignalJets_FailORFatjet,       "nSignalJets_FailORFatjet/I");
  ntupleTree->Branch("nSignalBJets_FailORFatjet",    &b_nSignalBJets_FailORFatjet,      "nSignalBJets_FailORFatjet/I");
  ntupleTree->Branch("nSignalLightJets_FailORFatjet",&b_nSignalLightJets_FailORFatjet,  "nSignalLightJets_FailORFatjet/I");
  ntupleTree->Branch("MET_pt",                  &b_MET_pt,               "MET_pt/F");
  ntupleTree->Branch("MET_phi",                 &b_MET_phi,              "MET_phi/F");
  ntupleTree->Branch("passMETFilters",          &b_passMETFilters,       "passMETFilters/O");
}
void JetTaggingTreeMaker::StoreNtupleTree(){
  ntupleFile->Write();
  ntupleFile->Close();
  std::cout << "Output File Saved " << std::endl;
}
int JetTaggingTreeMaker::EventLoop(int maxEvents){

  //Set Number of events to process. Take manual maxEvents if maxEvents is > 0 and less than the total number of events in the input files. 
  nEvents = (maxEvents > 0 && maxEvents < treeEvents) ? maxEvents : treeEvents;
  
  float eventWeightScale = _lumi * _xs * _kFactor / mcEventSumw;
  std::cout << "eventWeightScale = lumi * xs * kFactor / mcEventSumw = " << _lumi << " * " << _xs << " * " << _kFactor << " / " << mcEventSumw << " = " << eventWeightScale << std::endl;
  std::cout << "\nProcess " << nEvents << " of " << treeEvents << " events.\n";

  bool passLoadEvent       = true;
  bool passPreselection    = true;
  bool passEventHypothesis = true;
  bool passEvent           = true;

  for(long int e = 0; e < nEvents; e++)
  {
    // Periodically update status
    if( (e+1)%10000 == 0 || e+1==nEvents || debug){
      Monitor(e);
    }
    //
    // Reset Ntuple Variables
    //
    ResetNtupleVariables();
    //
    // Load event from ttree
    //
    passLoadEvent = eventReader->LoadEventFromTTree(e);
    if(!passLoadEvent) continue;
    //
    // passPreselection
    //   
    passPreselection = eventReader->PassPreselection();
    if (!passPreselection) continue;
    //
    // passEventHypothesis
    //
    passEventHypothesis = eventReader->ConstructEventHypothesis(); 
    if (!passEventHypothesis) continue;
    //
    // passEvent
    //
    passEvent = ProcessEvent();
    if(!passEvent) continue;
    //
    // Event pass all. Fill in ntuple.
    //
    FillNtupleVariables();
    ntupleTree->Fill();
  }
  std::cout << std::endl;
  minutes = static_cast<int>(duration/60);
  seconds = static_cast<int>(duration - minutes*60);             
  if(isMC){
    fprintf(stdout,"---------------------------\nProcessed %li events in %02i:%02i\n", nEvents, minutes, seconds);
  }else{
    fprintf(stdout,"---------------------------\nProcessed %li events (%.2f/fb) in %02i:%02i\n", nEvents, intLumi/1000, minutes, seconds);
  }
  return 0;
}
bool JetTaggingTreeMaker::ProcessEvent(){
  if(debug) std::cout << "ProcessEvent start" << std::endl;
  //
  // If MC
  //
  if(isMC){
    eventReader->evtWeight = eventReader->genWeight * (_lumi * _xs * _kFactor / mcEventSumw);
    if(debug) std::cout << "event->genWeight * (lumi * xs * kFactor / mcEventSumw) = " << eventReader->genWeight << " * (" << _lumi << " * " << _xs << " * " << _kFactor << " / " << mcEventSumw << ") = " << eventReader->evtWeight << std::endl;
    if(!(eventReader->passFatJetCand)){
      if(debug) std::cout << "Fail ProcessEvent: MC" << std::endl;
      return false;
    }
  }
  //
  //if we are processing data, first apply lumiMask and trigger
  //
  if(!isMC){
    if(!PassLumiMask()){
      if(debug) std::cout << "Fail lumiMask" << std::endl;
      return false;
    }
    if(!(eventReader->passFatJetCand)){
      if(debug) std::cout << "Fail ProcessEvent: data" << std::endl;
      return false;
    }
  }
  if(debug) std::cout << "ProcessEvent end" << std::endl;
  return true;
}
void JetTaggingTreeMaker::Monitor(long int e){
  //Monitor progress
  clock_current = std::chrono::steady_clock::now();
  time_span     = clock_current - clock_begin;
  nseconds      = double(time_span.count()) * std::chrono::steady_clock::period::num / std::chrono::steady_clock::period::den;
  elapsed_seconds = static_cast<int>(int(nseconds)%60);
  elapsed_minutes = static_cast<int>(nseconds/60); 
  
  percent        = (e+1)*100/nEvents;
  duration       = ( std::clock() - start ) / (double) CLOCKS_PER_SEC;
  eventRate      = (e+1)/duration;
  timeRemaining  = (nEvents-e)/eventRate;
  minutes = static_cast<int>(timeRemaining/60);
  seconds = static_cast<int>(timeRemaining - minutes*60);
  getrusage(who, &usage);
  usageMB = usage.ru_maxrss/1024;
  //print status and flush stdout so that status bar only uses one line
  fprintf(stdout, "\rProcessed: %8li of %li ( %2li%% | %.0f events/s | done in %02i:%02i | time elapsed %02i:%02i | memory usage: %li MB)  ", 
                                e+1, nEvents, percent,   eventRate,    minutes, seconds, elapsed_minutes, elapsed_seconds, usageMB);
  fflush(stdout);
}
bool JetTaggingTreeMaker::PassLumiMask(){
  // if the lumiMask is empty, then no JSON file was provided so all
  // events should pass
  if(_lumiMask.empty()) return true;

  //make lumiID run:lumiBlock
  edm::LuminosityBlockID lumiID(eventReader->run, eventReader->lumiBlock);

  //define function that checks if a lumiID is contained in a lumiBlockRange
  bool (*funcPtr) (edm::LuminosityBlockRange const &, edm::LuminosityBlockID const &) = &edm::contains;

  //Loop over the lumiMask and use funcPtr to check for a match
  std::vector< edm::LuminosityBlockRange >::const_iterator iter = std::find_if (_lumiMask.begin(), _lumiMask.end(), boost::bind(funcPtr, _1, lumiID) );

  return _lumiMask.end() != iter; 
}
void JetTaggingTreeMaker::FillNtupleVariables(){
  b_run                       = eventReader->run;
  b_lumiBlock                 = eventReader->lumiBlock;
  b_event                     = eventReader->event;
  
  b_nPVs                      = eventReader->nPVs;
  b_nPVsGood                  = eventReader->nPVsGood;
  
  if(isMC){
    b_mcKFactor                 = _kFactor;
    b_mcXS                      = _xs;
    b_mcGenWeight               = eventReader->genWeight;
  }

  b_evtWeight                 = eventReader->evtWeight;

  b_MET_pt  = eventReader->MET_pt;
  b_MET_phi = eventReader->MET_phi;
  b_passMETFilters = eventReader->passMETFilters;
}
void JetTaggingTreeMaker::ResetNtupleVariables(){

  b_run = -9;
  b_lumiBlock = -9;
  b_event = -9;

  b_nPVs = -9;
  b_nPVsGood = -9;

  b_mcKFactor = 1.0;
  b_mcXS = 1.0;
  b_mcGenWeight = 1.0;

  b_evtWeight = 1.0;

  b_MET_pt = -99.;
  b_MET_phi = -99.;
  b_passMETFilters = false;
}

JetTaggingTreeMaker::~JetTaggingTreeMaker(){} 