interface ProtocolData {
  tvl: number
  audits: number
  liquidity: number
  socialSentiment: number
}

interface RiskAnalysis {
  score: string
  metrics: string
}

function calculateRiskScore(data: ProtocolData): string {
  const { tvl, audits, liquidity, socialSentiment } = data

  // Weighted scoring system
  const score = tvl * 0.4 + audits * 0.3 + liquidity * 0.2 + socialSentiment * 0.1

  if (score >= 80) return '🟢 Safe'
  if (score >= 50) return '🟡 Moderate Risk'
  return '🔴 High Risk'
}

function extractKeyMetrics(data: ProtocolData): string {
  return `
    Total Value Locked: $${data.tvl.toLocaleString()}
    Audits: ${data.audits}
    Liquidity: $${data.liquidity.toLocaleString()}
    Social Sentiment: ${data.socialSentiment.toFixed(2)}/10
  `
}

export default defineEventHandler(async (event) => {
  const body = await readBody(event)

  // You'll need to implement this function to fetch data from DeFi Llama API
  const protocolData = await fetchProtocolData(body.protocolName)

  const riskScore = calculateRiskScore(protocolData)
  const metrics = extractKeyMetrics(protocolData)

  return {
    score: riskScore,
    metrics: metrics,
  }
})
