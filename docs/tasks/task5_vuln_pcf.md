# Task 5 — 5G Code Security Review: PCF OAM Endpoint

**ID:** task5_vuln_pcf  
**Tipo:** textual  
**Difficoltà:** media

---

## Scenario

The following Go code is part of the **PCF (Policy Control Function)**, a Network Function (NF) of the 5G core. It implements the SBI (Service-Based Interface) HTTP handler for the OAM (Operations, Administration and Maintenance) endpoint `/am-policy/:supi`, used to retrieve the Access & Mobility policy of a subscriber identified by SUPI. The handler is built with the Gin web framework.

File: `PCF/api_oam.go`

```go
const (
	CorsConfigMaxAge = 86400
)

func (s *Server) setCorsHeader(c *gin.Context) {
	// TODO: 1. turn these values into configurable variables
	// TODO: 2. use the official cors middleware
	s.router.Use(cors.New(cors.Config{
		AllowMethods: []string{"GET", "POST", "OPTIONS", "PUT", "PATCH", "DELETE"},
		AllowHeaders: []string{
			"Origin", "Content-Length", "Content-Type", "User-Agent",
			"Referrer", "Host", "Token", "X-Requested-With",
		},
		ExposeHeaders:    []string{"Content-Length"},
		AllowCredentials: true,
		AllowAllOrigins:  true,
		MaxAge:           CorsConfigMaxAge,
	}))

	c.Writer.Header().Set("Access-Control-Allow-Origin", "*")
	c.Writer.Header().Set("Access-Control-Allow-Credentials", "true")
	c.Writer.Header().Set(
		"Access-Control-Allow-Headers", "Content-Type, Content-Length, Accept-Encoding, "+
			"X-CSRF-Token, Authorization, accept, origin, Cache-Control, X-Requested-With")
	c.Writer.Header().Set("Access-Control-Allow-Methods", "POST, OPTIONS, GET, PUT, PATCH, DELETE")
}

func (s *Server) HTTPOAMGetAmPolicy(c *gin.Context) {
	s.setCorsHeader(c)

	supi := c.Params.ByName("supi")
	if supi == "" {
		problemDetails := &models.ProblemDetails{
			Title:  util.ERROR_INITIAL_PARAMETERS,
			Status: http.StatusBadRequest,
		}
		c.Set(sbi.IN_PB_DETAILS_CTX_STR, problemDetails.Title)
		c.JSON(int(problemDetails.Status), problemDetails)
		return
	}
	s.Processor().HandleOAMGetAmPolicyRequest(c, supi)
}
```

---

## Question

1. Identify any security vulnerability in this code (cite the relevant lines/configuration).
2. Assess the concrete impact in the context of a 5G core deployment.
3. Propose a specific fix.

---

## Agent Instructions

Reply ONLY in JSON format:

```json
{
  "answer": {
    "vulnerability": "...",
    "impact": "...",
    "fix": "..."
  },
  "reasoning": "...",
  "confidence": 0.0
}
```
