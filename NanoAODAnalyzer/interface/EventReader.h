// -*- C++ -*-
#if !defined(EventReader_H)
#define EventReader_H

#include <iostream>

#include <TChain.h>
#include <TFile.h>
#include <TLorentzVector.h>
#include "NanoAODAnalysis/NanoAODAnalyzer/interface/InitBranch.h"
#include "NanoAODAnalysis/NanoAODAnalyzer/interface/RecoMuonReader.h"
#include "NanoAODAnalysis/NanoAODAnalyzer/interface/RecoElectronReader.h"
#include "NanoAODAnalysis/NanoAODAnalyzer/interface/RecoJetReader.h"
#include "NanoAODAnalysis/NanoAODAnalyzer/interface/RecoFatJetReader.h"
#include "NanoAODAnalysis/NanoAODAnalyzer/interface/RecoMETReader.h"
#include "NanoAODAnalysis/NanoAODAnalyzer/interface/TrigObjectReader.h"
#include "NanoAODAnalysis/NanoAODAnalyzer/interface/GenParticleReader.h"
#include "NanoAODAnalysis/NanoAODAnalyzer/interface/HelperFunctions.h"

using namespace NanoAODAnalysis;

namespace JetTaggingAnalysis {

  enum channel {   
    undefined = -1,
    muChan = 1, 
    elChan = 2, 
  };

  class EventReader {

  public:
    // Member variables
    TChain* tree;
    bool isMC;
    std::string eraName;
    bool debug;

    UInt_t    run       =  0;
    UInt_t    lumiBlock =  0;
    ULong64_t event     =  0;
    Int_t     nPVs      =  0;
    Int_t     nPVsGood  =  0;
    Float_t   genWeight =  1.0;
    Float_t   Pileup_nTrueInt = 0.0;

    Float_t   evtWeight =  1.0;

    RecoMuonReader*      readerMuons;
    RecoElectronReader*  readerElectrons;
    RecoJetReader*       readerJets;
    RecoFatJetReader*    readerFatJets;
    RecoMETReader*       readerMET;
    TrigObjectReader*    readerTrigObjects;
    GenParticleReader*   readerGenParticles;
   
    //============================================
    //
    // Pre-selection
    //
    //============================================
    bool passPreselTriggers = false;
    bool passPreselLeptons  = false;

    //============================================
    //
    // Lepton selection
    //
    //============================================
    std::vector< RecoMuonPtr >     recoMuons;
    std::vector< RecoElectronPtr > recoElectrons;

    unsigned int nRecoMuons     = 0;
    unsigned int nRecoElectrons = 0;
    unsigned int nRecoLeptons   = 0;

    RecoMuonPtr muon = nullptr;

    channel lepChan = undefined;
    float lepSF = 1.0;
    TLorentzVector tlv_lepton;

    bool passOneLepton = false;
    //============================================
    //
    // Trigger selection
    //
    //============================================
    std::vector< TrigObjectPtr >   trigObjectsMuon;
    std::vector< TrigObjectPtr >   trigObjectsElectron;
    bool lepIsTrigMatch = false;

    bool HLT_Mu50 = false;
    bool HLT_TkMu50 = false;

    bool passTrigHLT        = false;
    bool passTrigMatch      = false;
    bool passTrigger        = false;
    //============================================
    //
    // Object selection for fatjets
    //
    //============================================
    std::vector< RecoFatJetPtr > recoFatJets;
    std::vector< RecoFatJetPtr > signalFatJets;
    unsigned int nRecoFatJets   = 0;
    unsigned int nSignalFatJets = 0;

    //============================================
    // Hadronic Top/W Candidate
    //============================================
    RecoFatJetPtr fatjet   = nullptr;
    TLorentzVector tlv_fatjet;
    float fatjet_msoftdrop = -1.0;
    float fatjet_n2b1 = -9.0;
    float fatjet_n3b1 = -9.0;
    float fatjet_tau1 = -9.0;
    float fatjet_tau2 = -9.0;
    float fatjet_tau3 = -9.0;
    float fatjet_deepTag_TvsQCD = -9.0;
    float fatjet_deepTag_WvsQCD = -9.0;

    bool passFatJetCand = false;
    //============================================
    //
    // Object selection for jets 
    //
    //============================================
    std::vector< RecoJetPtr > recoJets;
    std::vector< RecoJetPtr > signalJets;
    unsigned int nRecoJets         = 0;
    unsigned int nSignalJets       = 0;

    std::vector< RecoJetPtr > signalJets_PassORFatjet;
    std::vector< RecoJetPtr > signalBJets_PassORFatjet;
    std::vector< RecoJetPtr > signalLightJets_PassORFatjet;
    unsigned int nSignalJets_PassORFatjet      = 0;
    unsigned int nSignalBJets_PassORFatjet     = 0;
    unsigned int nSignalLightJets_PassORFatjet = 0;

    RecoJetPtr   jet0_passORFatjet  = nullptr;
    TLorentzVector tlv_jet0_passORFatjet;
    bool jet0_passORFatjet_isBTag  = false;
    float jet0_passORFatjet_sfBTag = 1.0;

    std::vector< RecoJetPtr > signalJets_FailORFatjet;
    std::vector< RecoJetPtr > signalBJets_FailORFatjet;
    std::vector< RecoJetPtr > signalLightJets_FailORFatjet;
    unsigned int nSignalJets_FailORFatjet      = 0;
    unsigned int nSignalBJets_FailORFatjet     = 0;
    unsigned int nSignalLightJets_FailORFatjet = 0;

    //============================================
    //
    // MET and its filters
    //
    //============================================
    float MET_pt  = -9.;
    float MET_phi = -9.0;
    TLorentzVector tlv_MET;

    bool Flag_goodVertices = false;
    bool Flag_globalSuperTightHalo2016Filter = false;
    bool Flag_HBHENoiseFilter = false;
    bool Flag_HBHENoiseIsoFilter = false;
    bool Flag_EcalDeadCellTriggerPrimitiveFilter = false;
    bool Flag_BadPFMuonFilter = false;
    bool Flag_eeBadScFilter = false;

    bool passMETFilters     = false;
    //============================================
    //
    // Leptonic W reconstruction
    //
    //============================================
    float nu_pz = 0.0;
    float nu_E  = 0.0;

    TLorentzVector tlv_nu;
    TLorentzVector tlv_Wlep;
    //============================================
    //
    // Cut values
    //
    //============================================
    const float muonPtMin      = 30;
    const float muonEtaMax     = 2.4;
    const int   muonID         = 2;// Medium
    const int   muonISO        = -1;// No Isolation

    const float elecPtMin      = 30;
    const float elecEtaMax     = 2.5;
    const int   elecID         = 4;// Tight

    const float centralJetPtMin   = 25;
    const float centralJetEtaMin  = 0.0;
    const float centralJetEtaMax  = 2.4;
    //
    // https://twiki.cern.ch/twiki/bin/viewauth/CMS/BtagRecommendation80XReReco
    //
    // const float centralJetCSVv2Cut = 0.5426; // Loose
    const float centralJetCSVv2Cut = 0.8484; // Medium 
    // const float centralJetCSVv2Cut = 0.9535; // Tight

    const float fatjetPtMin   = 200;
    const float fatjetEtaMin  = 0.0;
    const float fatjetEtaMax  = 2.4;

    const float trigMatchDR = 0.15;

    // Constructors and member functions
    EventReader(TChain*, bool, std::string, bool); 
    bool LoadEventFromTTree(int);
    bool PassPreselection();
    bool ConstructEventHypothesis();
    void LoadEvent(int e);
    float CalculateNeutrinoPz();

    ~EventReader(); 
  };
}
#endif // EventReader_H