#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"
#include "Math/Vector4D.h"
#include <vector>

using namespace ROOT::VecOps;
using RNode = ROOT::RDF::RNode;
using rvec_p4 = const RVec<ROOT::Math::PtEtaPhiMVector> &;
using rvec_f  = const RVec<float> &;
using rvec_i  = const RVec<int> &;
using namespace std;

//
//
//
RVec<int> GetMotherPDGID(rvec_i genPartIdxMother, rvec_i pdgId)
{ 
  RVec<int> MotherPDGID;
  for (size_t i = 0; i < genPartIdxMother.size(); i++){
    if (genPartIdxMother[i] >= 0){
      MotherPDGID.emplace_back(pdgId[genPartIdxMother[i]]);
    }
    else{
      MotherPDGID.emplace_back(0);
    }
  }  
  return MotherPDGID;
}

//
//
//
RVec<float> MSoftRaw(
  rvec_i  FatJet_subJetIdx1,
  rvec_i  FatJet_subJetIdx2,
  rvec_f  SubJet_pt, 
  rvec_f  SubJet_eta, 
  rvec_f  SubJet_phi,
  rvec_f  SubJet_mass,
  rvec_f  SubJet_rawFactor
){
  RVec<float> vec_msoft_raw;
  vec_msoft_raw.reserve(FatJet_subJetIdx1.size());

  for (size_t i = 0; i < FatJet_subJetIdx1.size(); i++)
  {
    const int& idx1 = FatJet_subJetIdx1[i];
    const int& idx2 = FatJet_subJetIdx2[i];

    float msoft_raw = -1.;

    if (idx1 >= 0 && idx2 >= 0){
      float sf1 = 1.-SubJet_rawFactor[idx1];
      float sf2 = 1.-SubJet_rawFactor[idx2];
      ROOT::Math::PtEtaPhiMVector subjet1(sf1*SubJet_pt[idx1], SubJet_eta[idx1], SubJet_phi[idx1], sf1*SubJet_mass[idx1]);
      ROOT::Math::PtEtaPhiMVector subjet2(sf2*SubJet_pt[idx2], SubJet_eta[idx2], SubJet_phi[idx2], sf2*SubJet_mass[idx2]);
      msoft_raw = (subjet1+subjet2).M();
    }

    vec_msoft_raw.emplace_back(msoft_raw);
  }
  return vec_msoft_raw;
}

//
//
//
RVec<float> MSoftGenJetAK8(
  rvec_f  GenJetAK8_eta,
  rvec_f  GenJetAK8_phi,
  rvec_f  SubGenJetAK8_pt, 
  rvec_f  SubGenJetAK8_eta, 
  rvec_f  SubGenJetAK8_phi,
  rvec_f  SubGenJetAK8_mass
){
  RVec<float> vec_msoft;
  vec_msoft.reserve(GenJetAK8_eta.size());

  for (size_t i = 0; i < GenJetAK8_eta.size(); i++)
  {
    int idx1 = -1;
    int idx2 = -1;

    float msoft = -1.;

    for (size_t ii = 0; ii < SubGenJetAK8_pt.size(); ii++)
    {
      float dR = ROOT::VecOps::DeltaR(GenJetAK8_eta[i], SubGenJetAK8_eta[ii], GenJetAK8_phi[i], SubGenJetAK8_phi[ii]);
      if (dR > 0.8) continue;
      if (idx1 < 0) idx1 = ii;
      else if (idx1 >= 0 && idx2 < 0) idx2 = ii;
    }

    if (idx1 >= 0 && idx2 >= 0){
      ROOT::Math::PtEtaPhiMVector subjet1(SubGenJetAK8_pt[idx1], SubGenJetAK8_eta[idx1], SubGenJetAK8_phi[idx1], SubGenJetAK8_mass[idx1]);
      ROOT::Math::PtEtaPhiMVector subjet2(SubGenJetAK8_pt[idx2], SubGenJetAK8_eta[idx2], SubGenJetAK8_phi[idx2], SubGenJetAK8_mass[idx2]);
      msoft = (subjet1+subjet2).M();
    }

    vec_msoft.emplace_back(msoft);
  }
  return vec_msoft;
}
//
//
//
RVec<RVec<float>> MatchedGenJetAK8Kin(
  rvec_i  FatJet_genJetAK8Idx,
  rvec_f  GenJetAK8_pt, 
  rvec_f  GenJetAK8_msoftdrop
){
  RVec<RVec<float>> FatJet_MatchedGenJetAK8_Kin;
  RVec<float> vec_MatchedGenJetAK8_Pt;
  RVec<float> vec_MatchedGenJetAK8_MSoftDrop;

  vec_MatchedGenJetAK8_Pt.reserve(FatJet_genJetAK8Idx.size());
  vec_MatchedGenJetAK8_MSoftDrop.reserve(FatJet_genJetAK8Idx.size());

  for (size_t i = 0; i < FatJet_genJetAK8Idx.size(); i++)
  {
    const int& idx = FatJet_genJetAK8Idx[i];

    if(FatJet_genJetAK8Idx[i]>=0){
      vec_MatchedGenJetAK8_Pt.emplace_back(GenJetAK8_pt[idx]);
      vec_MatchedGenJetAK8_MSoftDrop.emplace_back(GenJetAK8_msoftdrop[idx]);
    }else{
      vec_MatchedGenJetAK8_Pt.emplace_back(-1.);
      vec_MatchedGenJetAK8_MSoftDrop.emplace_back(-1.);
    }
  }

  FatJet_MatchedGenJetAK8_Kin.emplace_back(vec_MatchedGenJetAK8_Pt);
  FatJet_MatchedGenJetAK8_Kin.emplace_back(vec_MatchedGenJetAK8_MSoftDrop);
  return FatJet_MatchedGenJetAK8_Kin;
}

//
// Right way to do multiple branches for objects in a single loop function
//
RVec<RVec<int>> FatJetGenFlavourLabels(
  rvec_f  FatJet_eta, 
  rvec_f  FatJet_phi, 
  rvec_f  GenPart_eta,
  rvec_f  GenPart_phi,
  rvec_i  GenPart_isWBoson,
  rvec_i  GenPart_isZBoson,
  rvec_i  GenPart_isQFromWBoson,
  rvec_i  GenPart_isQFromZBoson
)
{ 
  RVec<RVec<int>> FatJet_FlavourLabels;
  RVec<int> FlavourLabelW;
  RVec<int> FlavourLabelZ;

  FlavourLabelW.reserve(FatJet_eta.size());
  FlavourLabelZ.reserve(FatJet_eta.size());

  for (size_t i = 0; i < FatJet_eta.size(); i++)
  {
    bool hasWBoson  = false;
    bool hasQ1FromW = false;
    bool hasQ2FromW = false;

    bool hasZBoson  = false;
    bool hasQ1FromZ = false;
    bool hasQ2FromZ = false;


    for (size_t ii = 0; ii < GenPart_eta.size(); ii++)
    {
      float dR = ROOT::VecOps::DeltaR(FatJet_eta[i], GenPart_eta[ii], FatJet_phi[i], GenPart_phi[ii]);
      if (dR > 0.8) continue;
      
      //
      // W-Boson
      //
      if (GenPart_isWBoson[ii]) hasWBoson = true;
      if (GenPart_isQFromWBoson[ii] && !hasQ1FromW) hasQ1FromW = true;
      else if (GenPart_isQFromWBoson[ii] && hasQ1FromW && !hasQ2FromW) hasQ2FromW = true;

      //
      // Z-Boson
      //
      if (GenPart_isZBoson[ii]) hasZBoson = true;
      if (GenPart_isQFromZBoson[ii] && !hasQ1FromZ) hasQ1FromZ = true;
      else if (GenPart_isQFromZBoson[ii] && hasQ1FromZ && !hasQ2FromZ) hasQ2FromZ = true;
    }

    if (hasWBoson && hasQ1FromW && hasQ2FromW) FlavourLabelW.emplace_back(1); 
    else FlavourLabelW.emplace_back(0);

    if (hasZBoson && hasQ1FromZ && hasQ2FromZ) FlavourLabelZ.emplace_back(1); 
    else FlavourLabelZ.emplace_back(0);
  }  
  
  FatJet_FlavourLabels.emplace_back(FlavourLabelW);
  FatJet_FlavourLabels.emplace_back(FlavourLabelZ);
  
  return FatJet_FlavourLabels;
}
//
//Incorret way to do multiple branches for objects in a single loop function
//
/*
RVec<RVec<int>> FatJetGenFlavourLabels(
  rvec_f  FatJet_eta, 
  rvec_f  FatJet_phi, 
  rvec_f  GenPart_eta,
  rvec_f  GenPart_phi,
  rvec_i  GenPart_isWBoson,
  rvec_i  GenPart_isZBoson,
  rvec_i  GenPart_isQFromWBoson,
  rvec_i  GenPart_isQFromZBoson
)
{ 
  RVec<RVec<int>> FatJet_FlavourLabels;
  FatJet_FlavourLabels.reserve()

  for (size_t i = 0; i < FatJet_eta.size(); i++)
  {
    bool hasWBoson  = false;
    bool hasQ1FromW = false;
    bool hasQ2FromW = false;

    bool hasZBoson  = false;
    bool hasQ1FromZ = false;
    bool hasQ2FromZ = false;

    RVec<int> FlavourLabels;

    for (size_t ii = 0; ii < GenPart_eta.size(); ii++)
    {
      float dR = ROOT::VecOps::DeltaR(FatJet_eta[i], GenPart_eta[ii], FatJet_phi[i], GenPart_phi[ii]);
      if (dR > 0.8) continue;
      
      //
      // W-Boson
      //
      if (GenPart_isWBoson[ii]) hasWBoson = true;
      if (GenPart_isQFromWBoson[ii] && !hasQ1FromW) hasQ1FromW = true;
      else if (GenPart_isQFromWBoson[ii] && hasQ1FromW && !hasQ2FromW) hasQ2FromW = true;

      //
      // Z-Boson
      //
      if (GenPart_isZBoson[ii]) hasZBoson = true;
      if (GenPart_isQFromZBoson[ii] && !hasQ1FromZ) hasQ1FromZ = true;
      else if (GenPart_isQFromZBoson[ii] && hasQ1FromZ && !hasQ2FromZ) hasQ2FromZ = true;
    }

    FlavourLabels = {
      hasWBoson && hasQ1FromW && hasQ2FromW,
      hasZBoson && hasQ1FromZ && hasQ2FromZ,
    };
    FatJet_FlavourLabels.emplace_back(FlavourLabels);
  }  
  return FatJet_FlavourLabels;
}
*/