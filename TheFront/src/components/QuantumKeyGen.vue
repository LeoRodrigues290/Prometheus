<template>
  <div class="flex flex-col items-center justify-center min-h-screen bg-dark-bg text-white">
    <h2 class="text-3xl font-bold mb-4">Gerar Chave Quântica</h2>
    <button @click="generateKey" class="bg-dark-highlight px-6 py-2 rounded hover:bg-dark-accent transition-colors">
      Gerar Nova Chave
    </button>

    <div v-if="quantumKey" class="mt-4 bg-dark-surface p-4 rounded text-center">
      <p class="break-all">
        <strong>Chave Gerada:</strong> {{ quantumKey }}
      </p>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'QuantumKeyGen',
  data() {
    return {
      quantumKey: ''
    }
  },
  methods: {
    async generateKey() {
      try {
        const token = localStorage.getItem('jwt_token')
        const response = await axios.get('http://localhost:8000/pyramid/generate_key', {
          headers: {
            Authorization: `Bearer ${token}`
          }
        })
        this.quantumKey = response.data.quantum_key
      } catch (error) {
        console.error(error)
        alert('Falha ao gerar chave quântica.')
      }
    }
  }
}
</script>
