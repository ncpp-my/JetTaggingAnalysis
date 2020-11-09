#include <iostream>
#include <fstream>
#include <string>
#include <iomanip>
#include <unordered_map>

#include <TROOT.h>
#include <TFile.h>
#include "TSystem.h"
#include "TChain.h"

#include "DataFormats/FWLite/interface/Event.h"
#include "DataFormats/FWLite/interface/Handle.h"
#include "DataFormats/FWLite/interface/InputSource.h"
#include "DataFormats/FWLite/interface/OutputFiles.h"

#include "FWCore/FWLite/interface/FWLiteEnabler.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/PythonParameterSet/interface/MakeParameterSets.h"

#include "PhysicsTools/FWLite/interface/TFileService.h"

#include "JetTaggingAnalysis/NanoAODAnalyzer/interface/JetTaggingTreeMaker.h"

using std::unordered_map;
using namespace JetTaggingAnalysis;

float GetMCXS(std::string);
float GetMCkFactor(std::string);

int main(int argc, char * argv[])
{
  gSystem->Load( "libFWCoreFWLite" );
  FWLiteEnabler::enable();

  // parse arguments
  if ( argc < 4 ) 
  {
    std::cout << "Usage : " << argv[0] << " [parameters.py]" << " [sampleName] " << " [sampleNameForXS] " << std::endl;
    return 0;
  }

  //
  // get the python configuration
  //
  if( !edm::readPSetsFrom(argv[1])->existsAs<edm::ParameterSet>("process") ){
    std::cout << " ERROR: ParametersSet 'process' is missing in your configuration file" << std::endl; exit(0);
  }  
  const edm::ParameterSet& process    = edm::readPSetsFrom(argv[1])->getParameter<edm::ParameterSet>("process");
  //
  //
  //
  const edm::ParameterSet& parameters = process.getParameter<edm::ParameterSet>("ProcessNanoAOD_JetTagging"); 
  std::string inputListDir     = parameters.getParameter<std::string>("inputListDir");
  std::string outputListDir    = parameters.getParameter<std::string>("outputListDir");
  int maxEvents = parameters.getParameter<int>("maxEvents");
  bool debug    = parameters.getParameter<bool>("debug");
  bool isMC     = parameters.getParameter<bool>("isMC");
  std::string era = parameters.getParameter<std::string>("era");
  bool blind = false;
  
  //
  //lumiMask: Only for data
  // 
  const edm::ParameterSet& inputs = process.getParameter<edm::ParameterSet>("inputs");   
  std::vector<edm::LuminosityBlockRange> lumiMask;
  if( !isMC && inputs.exists("lumisToProcess") ){
    std::vector<edm::LuminosityBlockRange> const & lumisTemp = inputs.getUntrackedParameter<std::vector<edm::LuminosityBlockRange> > ("lumisToProcess");
    lumiMask.resize( lumisTemp.size() );
    copy( lumisTemp.begin(), lumisTemp.end(), lumiMask.begin() );
  }
  if(debug) for(auto lumiID: lumiMask) std::cout<<"lumiID "<<lumiID<<std::endl;

  //
  // NanoAOD input source
  // Get list of root files from txt file
  //
  std::string sampleName  = std::string(argv[2]); 
  std::string txtFileName = inputListDir + sampleName + ".txt";
  std::ifstream infile(txtFileName);
  std::cout<< txtFileName <<std::endl;
  
  TChain* eventsTree     = new TChain("Events");
  TChain* lumiBlocksTree = new TChain("LuminosityBlocks");
  
  for(std::string line; getline( infile, line ); ){
    //
    // Make the filename
    //
    std::string fileName = line;
    std::cout << "Input File: " << fileName.c_str() << std::endl;
    int e = eventsTree     ->AddFile(fileName.c_str());
    int l = lumiBlocksTree ->AddFile(fileName.c_str());
    if(e!=1 || l!=1){ std::cout << "ERROR1" << std::endl; return 1;}
    if(debug) std::cout<<"Added to TChain"<<std::endl;
  }
  
  //
  // Get total sumofweights
  //
  std::string sampleNameForXS           = std::string(argv[3]); 
  std::string txtFileNameSumOfWeights = inputListDir + sampleNameForXS + ".txt";
  std::ifstream infileSumOfWeights(txtFileNameSumOfWeights);
  std::cout<< txtFileNameSumOfWeights <<std::endl; 
  TChain* runsTree       = new TChain("Runs");
  for(std::string line; getline( infileSumOfWeights, line ); ){
    //
    // Make the filename
    //
    std::string fileName = line;
    std::cout << "Input File: " << fileName.c_str() << std::endl;
    int r = runsTree       ->AddFile(fileName.c_str());
    if(r!=1){ std::cout << "ERROR2" << std::endl; return 1;}
    if(debug) std::cout<<"Added to TChain"<<std::endl;
  }

  float MCXSec = GetMCXS(sampleNameForXS);
  float MCkFactor = GetMCkFactor(sampleNameForXS);

  std::string outFileName      = "Ntuple_"+sampleName+".root";
  std::string outFileNameFinal = outputListDir + outFileName;

  JetTaggingTreeMaker* treeMaker = new JetTaggingTreeMaker(eventsTree,runsTree,lumiBlocksTree, isMC, blind, era, debug);
  treeMaker->SetMCXS(MCXSec);
  treeMaker->SetMCkFactor(MCkFactor);
  treeMaker->SetLumiMask(lumiMask);
  treeMaker->CreateNtupleTree(outFileNameFinal);
  treeMaker->EventLoop(maxEvents);
  treeMaker->StoreNtupleTree();
  delete treeMaker;

  std::cout << "ProcessNanoAOD_JetTagging::DONE" << std::endl;

  return 0;
}
float GetMCXS(std::string sampleName){
  //
  // Cross-sections should be in picobarn (pb)
  //
  std::unordered_map<std::string, float> m_sampleXS;   
  //https://twiki.cern.ch/twiki/bin/view/LHCPhysics/TtbarNNLO#Top_quark_pair_cross_sections_at  
  //BR for W-boson from PDG(2018)
  m_sampleXS["MC16_TT_2L"] = 831.76*(3*0.1086)*(3*0.1086);             
  m_sampleXS["MC16_TT_1L"] = 831.76*2*(3*0.1086*0.6741); 
  m_sampleXS["MC16_TT_0L"] = 831.76*2*(0.6741*0.6741); 
  //
  // https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#W_jets
  //
  m_sampleXS["MC16_WJetsToLNu_HT-70To100"]    = 1270;
  m_sampleXS["MC16_WJetsToLNu_HT-100To200"]   = 1345;
  m_sampleXS["MC16_WJetsToLNu_HT-200To400"]   = 359.7;
  m_sampleXS["MC16_WJetsToLNu_HT-400To600"]   = 48.91;
  m_sampleXS["MC16_WJetsToLNu_HT-600To800"]   = 12.05;
  m_sampleXS["MC16_WJetsToLNu_HT-800To1200"]  = 5.501;
  m_sampleXS["MC16_WJetsToLNu_HT-1200To2500"] = 1.329;
  m_sampleXS["MC16_WJetsToLNu_HT-2500ToInf"]  = 0.03216;
  //https://cms-gen-dev.cern.ch/xsdb/?searchQuery=DAS=ST_tW_antitop_5f_NoFullyHadronicDecays_13TeV-powheg_TuneCUETP8M1
  //https://cms-gen-dev.cern.ch/xsdb/?searchQuery=DAS=ST_tW_top_5f_NoFullyHadronicDecays_13TeV-powheg_TuneCUETP8M1
  m_sampleXS["MC16_ST_tW_antitop"]            = 38.06;
  m_sampleXS["MC16_ST_tW_top"]                = 38.09;
  //https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SingleTopRefXsec#Single_top_t_channel_cross_secti
  m_sampleXS["MC16_ST_t-channel_antitop"]     = 80.95;
  m_sampleXS["MC16_ST_t-channel_top"]         = 136.02;
  //https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SingleTopRefXsec#Single_top_s_channel_cross_secti
  m_sampleXS["MC16_ST_s-channel"]             = 10.32*(3*0.1086);
  //https://github.com/jkarancs/B2GTTrees/blob/master/test/crab3/cross_sections.txt
  //https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns
  m_sampleXS["MC16_WWTo4Q"]       = 51.723;
  m_sampleXS["MC16_WWToLNuQQ"]    = 49.997;
  m_sampleXS["MC16_WWTo2L2Nu"]    = 12.178;
  m_sampleXS["MC16_WZTo1L1Nu2Q"]  = 10.71;
  m_sampleXS["MC16_WZTo2Q2Nu"]    = 6.488;
  m_sampleXS["MC16_WZTo2L2Q"]     = 5.595; 
  m_sampleXS["MC16_WZTo3LNu"]     = 4.430;
  m_sampleXS["MC16_WZTo1L3Nu"]    = 3.033;
  m_sampleXS["MC16_ZZTo4Q"]       = 6.842;
  m_sampleXS["MC16_ZZTo2Q2Nu"]    = 4.04;
  m_sampleXS["MC16_ZZTo2L2Q"]     = 3.22;
  m_sampleXS["MC16_ZZTo2L2Nu"]    = 0.564;
  m_sampleXS["MC16_ZZTo4L"]       = 1.212;

  float xsec = 1.0;
  if ( m_sampleXS.find(sampleName) == m_sampleXS.end() ) {
    xsec = 1.0;
  } else {
    xsec = m_sampleXS[sampleName];
  }
  return xsec;
}
float GetMCkFactor(std::string sampleName){
  
  float kFact = 1.0;

  std::unordered_map<std::string, float> m_samplekFact; 
  // https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#W_jets
  m_samplekFact["MC16_WJetsToLNu_HT-70To100"]    = 1.21;
  m_samplekFact["MC16_WJetsToLNu_HT-100To200"]   = 1.21;
  m_samplekFact["MC16_WJetsToLNu_HT-200To400"]   = 1.21;
  m_samplekFact["MC16_WJetsToLNu_HT-400To600"]   = 1.21;
  m_samplekFact["MC16_WJetsToLNu_HT-600To800"]   = 1.21;
  m_samplekFact["MC16_WJetsToLNu_HT-800To1200"]  = 1.21;
  m_samplekFact["MC16_WJetsToLNu_HT-1200To2500"] = 1.21;
  m_samplekFact["MC16_WJetsToLNu_HT-2500ToInf"]  = 1.21;
  if ( m_samplekFact.find(sampleName) == m_samplekFact.end() ) {
    kFact = 1.0;
  } else {
    kFact = m_samplekFact[sampleName];
  }
  return kFact;
}


