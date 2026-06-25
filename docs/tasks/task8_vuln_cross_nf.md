# Task 8 — Security Code Review: Cross-NF Vulnerability Propagation

**ID:** task8_vuln_cross_nf
**Tipo:** textual
**Difficoltà:** alta

---

## Scenario

During a security audit of a 5G core network, you are asked to review the input validation chain across two network functions involved in the **PDU Session Establishment** flow.

When a UE initiates a PDU session, the AMF triggers a subscription data retrieval sequence:

```
AMF  ──Nudm_SDM_Get──▶  UDM (HandleGetSmfSelectData)
                          │
                          └──Nudr_DR_Query──▶  UDR (HandleQuerySmfSelectData)
```

The `supi` (Subscription Permanent Identifier) originates from the AMF and flows through this chain. The UDM is the entry point; the UDR is the downstream consumer.

Below are three handler excerpts from the actual SBI layer of these two network functions.

---

**UDM — Handler A: `HandleGetAmData`**
*(Nudm_SDM_Get — AM subscription data)*

```go
func (s *Server) HandleGetAmData(c *gin.Context) {
    logger.SdmLog.Infof("Handle GetAmData")

    supi := c.Params.ByName("supi")
    if !validator.IsValidSupi(supi) {
        problemDetail := models.ProblemDetails{
            Title:  "Malformed request syntax",
            Status: http.StatusBadRequest,
            Detail: "Supi is invalid",
            Cause:  "MANDATORY_IE_INCORRECT",
        }
        logger.SdmLog.Warnln("Supi is invalid")
        c.JSON(int(problemDetail.Status), problemDetail)
        return
    }

    plmnIDStruct, problemDetails := s.getPlmnIDStruct(c.Request.URL.Query())
    if problemDetails != nil {
        c.JSON(int(problemDetails.Status), problemDetails)
        return
    }
    s.Processor().GetAmDataProcedure(c, supi, plmnID, supportedFeatures)
}
```

---

**UDM — Handler B: `HandleGetSmfSelectData`**
*(Nudm_SDM_Get — SMF selection subscription data)*

```go
func (s *Server) HandleGetSmfSelectData(c *gin.Context) {
    logger.SdmLog.Infof("Handle GetSmfSelectData")

    supi := c.Params.ByName("supi")

    plmnIDStruct, problemDetails := s.getPlmnIDStruct(c.Request.URL.Query())
    if problemDetails != nil {
        c.JSON(int(problemDetails.Status), problemDetails)
        return
    }
    var plmnID string
    if plmnIDStruct != nil {
        plmnID = plmnIDStruct.Mcc + plmnIDStruct.Mnc
    }
    supportedFeatures := c.Query("supported-features")

    s.Processor().GetSmfSelectDataProcedure(c, supi, plmnID, supportedFeatures)
}
```

---

**UDR — Handler C: `HandleQuerySmfSelectData`**
*(Nudr_DR_Query — SMF selection data, downstream of UDM)*

```go
func (s *Server) HandleQuerySmfSelectData(c *gin.Context) {
    logger.DataRepoLog.Tracef("Handle QuerySmfSelectData")

    collName := "subscriptionData.provisionedData.smfSelectionSubscriptionData"
    ueId := c.Params.ByName("ueId")
    if ueId == "" {
        util.EmptyUeIdProblemJson(c)
        return
    }
    servingPlmnId := c.Params.ByName("servingPlmnId")

    s.Processor().QuerySmfSelectDataProcedure(c, collName, ueId, servingPlmnId)
}
```

---

## Question

1. Compare Handler A and Handler B in UDM: what is the security difference between them?
2. Considering that Handler B feeds into Handler C (UDR), explain how a weakness in the UDM layer can propagate downstream to the UDR.
3. What class of attacker or misbehaving component could exploit this chain, and what could they achieve?

---

## Agent Instructions

Reply ONLY in JSON format:

```json
{
  "answer": {
    "udm_comparison": "...",
    "propagation": "...",
    "threat_actor": "..."
  },
  "reasoning": "...",
  "confidence": 0.0
}
```
