# Solution — Task 10 (Security Review: UDR SDM Subscription Handler — Wrong Collection Name)

**ID:** task10_vuln_udr_collname_sol  
**Usage:** rubric for judge agent, GT not exposed to the tested agent  
**CVE reference:** no public CVE mapped; CWE-706 (Use of Incorrectly-Resolved Name or Reference)

---

## Ground Truth

```json
{
  "answer": "HandleCreateSdmSubscriptions uses collName = 'subscriptionData.contextData.amfNon3gppAccess' — the collection for AMF non-3GPP access registration data. SDM subscriptions should be stored in a dedicated collection (e.g., 'subscriptionData.contextData.sdmSubscriptions'). At runtime, new SDM subscription documents are written into the AMF non-3GPP access collection, corrupting its schema and making the subscriptions unretrievable via normal SDM subscription queries.",
  "type": "textual_security_review"
}
```

## GT Rationale

### Finding — Wrong MongoDB collection name (CWE-706)

In `HandleCreateSdmSubscriptions`, line:

```go
collName := "subscriptionData.contextData.amfNon3gppAccess"
```

This is the collection name used by `HandleCreateAmfContextNon3gpp` — it stores `models.AmfNon3GppAccessRegistration` documents. `HandleCreateSdmSubscriptions` stores `models.SdmSubscription` documents. These are structurally and semantically incompatible types.

**What happens at runtime:**

1. A POST to `/subscription-data/:ueId/:servingPlmnId/sdm-subscriptions` deserializes a `SdmSubscription` struct and passes it with the wrong `collName` to `CreateSdmSubscriptionsProcedure`.
2. The procedure writes the `SdmSubscription` document into `subscriptionData.contextData.amfNon3gppAccess`.
3. Two consequences:
   a. **Data corruption**: The AMF non-3GPP access collection now contains SDM subscription documents mixed with AMF registration documents. Any subsequent query against this collection (e.g., AMF non-3GPP access lookups) may return unexpected document types, causing type assertion failures or silent data leakage.
   b. **Subscription loss**: SDM subscriptions created via this endpoint are invisible to `HandleQuerysdmsubscriptions` (which queries the correct SDM subscriptions collection). NFs that registered for change notifications will not receive them, breaking the UDM→UDR change notification path and causing silent subscription failures.

**Impact in 5G context:**
- SDM subscriptions are the mechanism by which UDM (and other NFs) receive data change events from the UDR. If subscriptions are silently stored in the wrong collection, notifications are never delivered. This can cause UDM caches to become stale, leading to UEs receiving outdated policy data or failed re-authentication.
- Write to the wrong collection can corrupt AMF non-3GPP access records if MongoDB's collection is not strictly schema-enforced (which it is not by default in free5GC's use of BSON). Queries on corrupted documents may panic downstream handlers.

**Fix:** Change the collection name assignment to the correct collection:

```go
collName := "subscriptionData.contextData.sdmSubscriptions"
```

This matches the naming convention used elsewhere in the file for SDM-specific data and ensures documents are stored and retrieved from the correct collection.

---

## Rubric for the Judge Agent

The judge does NOT receive the explicit GT value. It receives: agent response + scenario + this rubric.

```json
{
  "rubrica": {
    "wrong_collection_identified_score": {
      "max": 4,
      "criteri": {
        "4": "Correctly identifies that collName = 'subscriptionData.contextData.amfNon3gppAccess' is the wrong collection for SDM subscriptions, names the correct expected collection (or gives a well-reasoned alternative), and explicitly contrasts it with HandleCreateAmfContextNon3gpp which legitimately uses that collection",
        "3": "Correctly identifies that the collection name is wrong and explains that SDM subscriptions should not go into the AMF non-3GPP collection, but does not specify the correct collection name",
        "2": "Identifies that the collection name looks suspicious or inconsistent with the handler's purpose without fully explaining why it is wrong",
        "1": "Vaguely notes something is wrong with the variable without identifying it as the collection name issue",
        "0": "Does not identify the wrong collection name"
      }
    },
    "runtime_impact_score": {
      "max": 3,
      "criteri": {
        "3": "Explains both consequences: (a) SDM subscription documents written to AMF collection causing schema corruption / unexpected query results, AND (b) subscriptions are invisible to query endpoints because they are in the wrong collection, breaking the notification path",
        "2": "Explains one of the two consequences accurately",
        "1": "Mentions that data will be misrouted without explaining the specific downstream effect",
        "0": "No runtime impact analysis or incorrect claim"
      }
    },
    "5g_context_score": {
      "max": 2,
      "criteri": {
        "2": "Explains the 5G impact: UDM change notifications will not be delivered because subscriptions are not found, causing stale caches or failed re-authentication; or correctly describes the role of SDM subscriptions in the UDR→UDM notification chain",
        "1": "Mentions generic data integrity or availability impact without 5G-specific detail",
        "0": "No 5G context or incorrect characterization"
      }
    },
    "fix_quality_score": {
      "max": 2,
      "criteri": {
        "2": "Proposes changing collName to the correct SDM subscriptions collection name (or a clearly justified equivalent), and optionally notes that a similar fix pattern exists elsewhere in the file",
        "1": "Suggests that the collection name should be changed without specifying the correct value",
        "0": "No fix proposed or fix is incorrect"
      }
    }
  },
  "total_max": 11
}
```
