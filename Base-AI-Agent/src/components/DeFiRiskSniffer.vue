<script setup lang="ts">
import { ref } from 'vue'

const userQuery = ref('')
const riskScore = ref('')
const riskMetrics = ref('')
const isLoading = ref(false)

async function checkProtocolSafety() {
  isLoading.value = true
  try {
    // Step 1: Fetch protocol data from DeFi Llama
    const protocolData = await fetchProtocolData(userQuery.value)

    // Step 2: Analyze data and generate risk score
    const analysis = await analyzeProtocolRisk(protocolData)

    // Step 3: Update UI with results
    riskScore.value = analysis.score
    riskMetrics.value = analysis.metrics
  } catch (error) {
    console.error('Error analyzing protocol:', error)
    riskScore.value = '🔴 Error'
  } finally {
    isLoading.value = false
  }
}

async function fetchProtocolData(protocolName: string) {
  // Implement DeFi Llama API call
  const response = await fetch(`https://api.llama.fi/protocol/${protocolName}`)
  return await response.json()
}

async function analyzeProtocolRisk(protocolData: any) {
  // Implement AI analysis logic
  const response = await fetch('/api/analyze-risk', {
    method: 'POST',
    body: JSON.stringify(protocolData),
  })
  return await response.json()
}
</script>

<template>
  <div class="defi-risk-sniffer">
    <h2>DeFi Risk Sniffer</h2>
    <div class="input-container">
      <input
        v-model="userQuery"
        placeholder="Is ProtocolX safe?"
        @keyup.enter="checkProtocolSafety"
      />
      <button @click="checkProtocolSafety" :disabled="isLoading">
        {{ isLoading ? 'Analyzing...' : 'Check Safety' }}
      </button>
    </div>

    <div v-if="riskScore" class="result-container">
      <div class="risk-score" :class="riskScore.toLowerCase()">Risk Score: {{ riskScore }}</div>
      <div v-if="riskMetrics" class="risk-metrics">
        <h3>Key Metrics:</h3>
        <pre>{{ riskMetrics }}</pre>
      </div>
    </div>
  </div>
</template>

<style scoped>
.defi-risk-sniffer {
  max-width: 600px;
  margin: 2rem auto;
  padding: 1rem;
  border: 1px solid var(--color-border);
  border-radius: 8px;
}

.input-container {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

input {
  flex: 1;
  padding: 0.5rem;
  border: 1px solid var(--color-border);
  border-radius: 4px;
}

button {
  padding: 0.5rem 1rem;
  background-color: var(--color-background-soft);
  border: 1px solid var(--color-border);
  border-radius: 4px;
  cursor: pointer;
}

button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.result-container {
  margin-top: 1rem;
  padding: 1rem;
  background-color: var(--color-background-mute);
  border-radius: 4px;
}

.risk-score {
  font-size: 1.2rem;
  font-weight: bold;
  margin-bottom: 1rem;
}

.risk-score.green {
  color: #4caf50;
}

.risk-score.yellow {
  color: #ffc107;
}

.risk-score.red {
  color: #f44336;
}

.risk-metrics pre {
  white-space: pre-wrap;
  word-wrap: break-word;
  background-color: var(--color-background);
  padding: 1rem;
  border-radius: 4px;
}
</style>
