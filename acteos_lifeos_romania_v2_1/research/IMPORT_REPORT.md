# Research Import Report

- generated_at: 2026-06-25T18:36:10.257279+00:00
- source: `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox`
- dest: `/Users/vaduvageorge/Desktop/ActeOs/acteos_lifeos_romania_v2_1/research/inbox`
- mode: import

## Counts

- discovered: 193
- imported (valid): 92
- rejected (invalid): 13
- skipped (duplicate/exists): 88

## Rejected (NOT imported)

### ro.life.early_retirement
- source: `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_11/ro.life.early_retirement`
  - rule rule.early.stage_not_met: Additional properties are not allowed ('note' was unexpected)

### ro.life.change_business_activity
- source: `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_12/ro.life.change_business_activity`
  - rule rule.activity.other_uat_local_gap: Additional properties are not allowed ('note' was unexpected)

### ro.life.change_company_address
- source: `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_12/ro.life.change_company_address`
  - rule rule.address.other_uat_local_gap: Additional properties are not allowed ('note' was unexpected)

### ro.life.close_working_point
- source: `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_12/ro.life.close_working_point`
  - rule rule.close_point.other_uat_local_gap: Additional properties are not allowed ('note' was unexpected)

### ro.life.open_working_point
- source: `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_12/ro.life.open_working_point`
  - rule rule.open_point.other_uat_local_gap: Additional properties are not allowed ('note' was unexpected)

### ro.life.resume_business
- source: `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_12/ro.life.resume_business`
  - rule rule.resume.other_uat_local_gap: Additional properties are not allowed ('note' was unexpected)

### ro.life.tax_decision_contest
- source: `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_13/ro.life.tax_decision_contest`
  - rule rule.b13.tax_contest.within_instruction: Additional properties are not allowed ('note' was unexpected)
  - rule rule.b13.tax_contest.after_instruction: Additional properties are not allowed ('note' was unexpected)

### ro.life.declare_vehicle_local_tax
- source: `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/r1a/ro.life.declare_vehicle_local_tax`
  - rule rule.vtax.salubritate_not_tm: Additional properties are not allowed ('note' was unexpected)

### ro.life.identity_card_change_address
- source: `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/r1a/ro.life.identity_card_change_address`
  - rule rule.addr.cei_no_new_doc: Additional properties are not allowed ('note' was unexpected)
  - rule rule.addr.resedinta: Additional properties are not allowed ('note' was unexpected)

### ro.life.identity_card_expired
- source: `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/r1a/ro.life.identity_card_expired`
  - rule rule.exp.sanction_conflict: Additional properties are not allowed ('note' was unexpected)

### ro.life.identity_card_lost
- source: `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/r1a/ro.life.identity_card_lost`
  - rule rule.lost.sanction_conflict: source_claim_id 'claim.exp.sanction_40_80' not found in source_claims.yaml

### ro.life.identity_card_stolen
- source: `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/r1a/ro.life.identity_card_stolen`
  - rule rule.lost.sanction_conflict: source_claim_id 'claim.exp.sanction_40_80' not found in source_claims.yaml

### ro.life.criminal_record_certificate
- source: `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/r1b/ro.life.criminal_record_certificate`
  - rule rule.cj.issuance_foreign: 'values' is a required property at /when

## Skipped

- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_01/ro.life.identity_theft_suspected` (ro.life.identity_theft_suspected): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_02/ro.life.consular_service` (ro.life.consular_service): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_02/ro.life.documents_legalisation_translation` (ro.life.documents_legalisation_translation): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_02/ro.life.documents_lost_abroad` (ro.life.documents_lost_abroad): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_02/ro.life.foreign_document_recognition` (ro.life.foreign_document_recognition): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_02/ro.life.renounce_citizenship` (ro.life.renounce_citizenship): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_02/ro.life.residence_registration_eu` (ro.life.residence_registration_eu): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_02/ro.life.residence_right_ro` (ro.life.residence_right_ro): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_02/ro.life.romanian_citizenship` (ro.life.romanian_citizenship): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_02/ro.life.transcribe_foreign_birth` (ro.life.transcribe_foreign_birth): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_02/ro.life.transcribe_foreign_death` (ro.life.transcribe_foreign_death): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_03/ro.life.adoption` (ro.life.adoption): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_03/ro.life.divorce_admin` (ro.life.divorce_admin): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_03/ro.life.family_death` (ro.life.family_death): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_03/ro.life.guardianship` (ro.life.guardianship): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_03/ro.life.inheritance_succession` (ro.life.inheritance_succession): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_03/ro.life.marriage_planning` (ro.life.marriage_planning): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_03/ro.life.name_change_after_marriage` (ro.life.name_change_after_marriage): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_03/ro.life.parental_authority_change` (ro.life.parental_authority_change): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_03/ro.life.spouse_death` (ro.life.spouse_death): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_03/ro.life.transcribe_foreign_marriage` (ro.life.transcribe_foreign_marriage): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_04/ro.life.minor_travel_abroad` (ro.life.minor_travel_abroad): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_07/ro.life.bought_home` (ro.life.bought_home): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_07/ro.life.rent_out_home` (ro.life.rent_out_home): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_07/ro.life.rented_home` (ro.life.rented_home): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_07/ro.life.return_to_romania` (ro.life.return_to_romania): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_07/ro.life.sold_home` (ro.life.sold_home): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_08/ro.life.building_permit` (ro.life.building_permit): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_08/ro.life.construction_reception` (ro.life.construction_reception): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_08/ro.life.construction_start_notice` (ro.life.construction_start_notice): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_08/ro.life.declare_home_local_tax` (ro.life.declare_home_local_tax): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_08/ro.life.declare_property_local_tax` (ro.life.declare_property_local_tax): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_08/ro.life.demolition_permit` (ro.life.demolition_permit): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_08/ro.life.house_extension` (ro.life.house_extension): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_08/ro.life.land_split_merge` (ro.life.land_split_merge): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_08/ro.life.property_cadastral_registration` (ro.life.property_cadastral_registration): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_08/ro.life.renovation_authorisation_check` (ro.life.renovation_authorisation_check): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_13/ro.life.beneficial_owner_update` (ro.life.beneficial_owner_update): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_13/ro.life.company_admin_personal_change` (ro.life.company_admin_personal_change): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_13/ro.life.company_vehicle_change` (ro.life.company_vehicle_change): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_13/ro.life.declare_rental_income` (ro.life.declare_rental_income): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_13/ro.life.pay_fine` (ro.life.pay_fine): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_13/ro.life.pay_local_taxes` (ro.life.pay_local_taxes): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_13/ro.life.tax_refund_request` (ro.life.tax_refund_request): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_13/ro.life.tax_return_individual` (ro.life.tax_return_individual): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_13/ro.life.vat_registration` (ro.life.vat_registration): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_14/ro.life.bought_new_vehicle` (ro.life.bought_new_vehicle): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_14/ro.life.import_vehicle_eu` (ro.life.import_vehicle_eu): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_14/ro.life.import_vehicle_non_eu` (ro.life.import_vehicle_non_eu): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_14/ro.life.temporary_vehicle_authorisation` (ro.life.temporary_vehicle_authorisation): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_14/ro.life.vehicle_deregistration` (ro.life.vehicle_deregistration): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_14/ro.life.vehicle_inheritance` (ro.life.vehicle_inheritance): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_14/ro.life.vehicle_plate_lost_stolen` (ro.life.vehicle_plate_lost_stolen): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_14/ro.life.vehicle_registration` (ro.life.vehicle_registration): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_14/ro.life.vehicle_registration_certificate_lost` (ro.life.vehicle_registration_certificate_lost): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_14/ro.life.vehicle_stolen` (ro.life.vehicle_stolen): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_16/ro.life.change_heat_holder` (ro.life.change_heat_holder): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_16/ro.life.change_internet_holder` (ro.life.change_internet_holder): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_16/ro.life.utility_connection_construction` (ro.life.utility_connection_construction): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_16/ro.life.utility_new_connection` (ro.life.utility_new_connection): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_17/ro.life.account_recovery_gov` (ro.life.account_recovery_gov): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_17/ro.life.bank_account_open` (ro.life.bank_account_open): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_17/ro.life.bank_card_change` (ro.life.bank_card_change): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_17/ro.life.bank_card_lost_stolen` (ro.life.bank_card_lost_stolen): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_17/ro.life.baptism` (ro.life.baptism): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_17/ro.life.digital_identity_ro` (ro.life.digital_identity_ro): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_17/ro.life.electronic_signature` (ro.life.electronic_signature): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_17/ro.life.home_insurance_claim` (ro.life.home_insurance_claim): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_17/ro.life.life_insurance_claim` (ro.life.life_insurance_claim): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_17/ro.life.religious_marriage` (ro.life.religious_marriage): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_18/ro.life.association_registration` (ro.life.association_registration): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_18/ro.life.domestic_violence_protection_order` (ro.life.domestic_violence_protection_order): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_18/ro.life.fishing_permit` (ro.life.fishing_permit): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_18/ro.life.foundation_registration` (ro.life.foundation_registration): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_18/ro.life.military_certificate` (ro.life.military_certificate): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_18/ro.life.military_enrollment` (ro.life.military_enrollment): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_18/ro.life.military_reserve_status` (ro.life.military_reserve_status): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_18/ro.life.radio_amateur_license` (ro.life.radio_amateur_license): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/batch_18/ro.life.weapon_permit` (ro.life.weapon_permit): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/r1a/ro.life.bought_used_vehicle_ro` (ro.life.bought_used_vehicle_ro): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/r1a/ro.life.local_tax_certificate` (ro.life.local_tax_certificate): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/r1a/ro.life.moved_home` (ro.life.moved_home): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/r1a/ro.life.sold_vehicle_ro` (ro.life.sold_vehicle_ro): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/r1a/ro.life.vehicle_change_address` (ro.life.vehicle_change_address): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/r1a/ro.life.vehicle_transcription` (ro.life.vehicle_transcription): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/r1b/ro.life.change_electricity_holder` (ro.life.change_electricity_holder): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/r1b/ro.life.change_gas_holder` (ro.life.change_gas_holder): destination already exists (use --overwrite)
- `/Users/vaduvageorge/Desktop/ActeOs/docs/product/lifeos-romania/research/inbox/r1b/ro.life.change_water_holder` (ro.life.change_water_holder): destination already exists (use --overwrite)

## Governance

The inbox is staging only. Nothing imported here is active. Promotion to
the active ruleset requires four-eyes review + the release gate
(skill: acteos-release-certification). `status: active` on a source rule
or claim is preserved verbatim but has no runtime effect until then.
