from ..quantities import nanoAOD as nanoAOD
from code_generation.producer import Producer, ProducerGroup


####################
# Set of producers used for selection of good boosted taus
####################

ConvertFatJetJetID = Producer(
    name="ConvertFatJetJetID",
    call='converters::cast<ROOT::VecOps::RVec<UChar_t>, ROOT::VecOps::RVec<int>>({df}, {input}, {output})',
    input=[nanoAOD.FatJet_ID_orig],
    output=[nanoAOD.FatJet_ID],
    scopes=["global"],
)

ConvertJetID = Producer(
    name="ConvertJetID",
    call='converters::cast<ROOT::VecOps::RVec<UChar_t>, ROOT::VecOps::RVec<int>>({df}, {input}, {output})',
    input=[nanoAOD.Jet_ID_orig],
    output=[nanoAOD.Jet_ID],
    scopes=["global"],
)

ConvertJetPUID = Producer(
    name="ConvertJetPUID",
    call='converters::cast<ROOT::VecOps::RVec<UChar_t>, ROOT::VecOps::RVec<int>>({df}, {input}, {output})',
    input=[nanoAOD.Jet_PUID_orig],
    output=[nanoAOD.Jet_PUID],
    scopes=["global"],
)

ConvertGenParticleStatusFlags = Producer(
    name="ConvertGenParticleStatusFlags",
    call='converters::cast<ROOT::VecOps::RVec<UShort_t>, ROOT::VecOps::RVec<int>>({df}, {input}, {output})',
    input=[nanoAOD.GenParticle_statusFlags_orig],
    output=[nanoAOD.GenParticle_statusFlags],
    scopes=["global"],
)

ConvertTauDecayMode = Producer(
    name="ConvertTauDecayMode",
    call='converters::cast<ROOT::VecOps::RVec<UChar_t>, ROOT::VecOps::RVec<int>>({df}, {input}, {output})',
    input=[nanoAOD.Tau_decayMode_orig],
    output=[nanoAOD.Tau_decayMode],
    scopes=["global"],
)

ConvertJetAssociatedGenJet = Producer(
    name="ConvertJetAssociatedGenJet",
    call='converters::cast<ROOT::VecOps::RVec<Short_t>, ROOT::VecOps::RVec<int>>({df}, {input}, {output})',
    input=[nanoAOD.Jet_associatedGenJet_orig],
    output=[nanoAOD.Jet_associatedGenJet],
    scopes=["global"],
)

ConvertGenJethadFlavour = Producer(
    name="ConvertGenJethadFlavour",
    call='converters::cast<ROOT::VecOps::RVec<UChar_t>, ROOT::VecOps::RVec<int>>({df}, {input}, {output})',
    input=[nanoAOD.GenJet_hadFlavour_orig],
    output=[nanoAOD.GenJet_hadFlavour],
    scopes=["global"],
)

ConvertFatJetFlavour = Producer(
    name="ConvertFatJetFlavour",
    call='converters::cast<ROOT::VecOps::RVec<UChar_t>, ROOT::VecOps::RVec<int>>({df}, {input}, {output})',
    input=[nanoAOD.FatJet_flavour_orig],
    output=[nanoAOD.FatJet_flavour],
    scopes=["global"],
)

ConvertGenParticleMotherid = Producer(
    name="ConvertGenParticleMotherid",
    call='converters::cast<ROOT::VecOps::RVec<Short_t>, ROOT::VecOps::RVec<int>>({df}, {input}, {output})',
    input=[nanoAOD.GenParticle_motherid_orig],
    output=[nanoAOD.GenParticle_motherid],
    scopes=["global"],
)

ConvertTauCharge = Producer(
    name="ConvertTauCharge",
    call='converters::cast<ROOT::VecOps::RVec<Short_t>, ROOT::VecOps::RVec<int>>({df}, {input}, {output})',
    input=[nanoAOD.Tau_charge_orig],
    output=[nanoAOD.Tau_charge],
    scopes=["global"],
)

ConvertTauAssociatedJet = Producer(
    name="ConvertTauAssociatedJet",
    call='converters::cast<ROOT::VecOps::RVec<Short_t>, ROOT::VecOps::RVec<int>>({df}, {input}, {output})',
    input=[nanoAOD.Tau_associatedJet_orig],
    output=[nanoAOD.Tau_associatedJet],
    scopes=["global"],
)

ConvertMuonIndexToGen = Producer(
    name="ConvertMuonIndexToGen",
    call='converters::cast<ROOT::VecOps::RVec<Short_t>, ROOT::VecOps::RVec<int>>({df}, {input}, {output})',
    input=[nanoAOD.Muon_indexToGen_orig],
    output=[nanoAOD.Muon_indexToGen],
    scopes=["global"],
)

ConvertTauIndexToGen = Producer(
    name="ConvertTauIndexToGen",
    call='converters::cast<ROOT::VecOps::RVec<Short_t>, ROOT::VecOps::RVec<int>>({df}, {input}, {output})',
    input=[nanoAOD.Tau_indexToGen_orig],
    output=[nanoAOD.Tau_indexToGen],
    scopes=["global"],
)

ConvertTriggerObjectID = Producer(
    name="ConvertTriggerObjectID",
    call='converters::cast<ROOT::VecOps::RVec<UShort_t>, ROOT::VecOps::RVec<int>>({df}, {input}, {output})',
    input=[nanoAOD.TriggerObject_id_orig],
    output=[nanoAOD.TriggerObject_id],
    scopes=["global"],
)


Convert = ProducerGroup(
    name="Convert",
    call=None,
    input=None,
    output=None,
    scopes=["global"],
    subproducers=[
        ConvertFatJetJetID,
        ConvertJetID,
        ConvertJetPUID,
        ConvertGenParticleStatusFlags,
        ConvertTauDecayMode,
        ConvertJetAssociatedGenJet,
        ConvertGenJethadFlavour,
        ConvertFatJetFlavour,
        ConvertGenParticleMotherid,
        ConvertTauCharge,
        ConvertTauAssociatedJet,
        ConvertMuonIndexToGen,
        ConvertTauIndexToGen,
        ConvertTriggerObjectID,
    ],
)