<template>
  <div>
    <form @submit.prevent="handleLogin">
      <input v-model="email" placeholder="Email" />
      <input v-model="password" type="password" placeholder="Senha" />
      <button type="submit">Entrar</button>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { login } from '../services/auth'

const email = ref('')
const password = ref('')

async function handleLogin() {
  try {
    const result = await login(email.value, password.value)
    console.log('Login bem-sucedido:', result)
    alert('Login bem-sucedido')
    // this.$router.push('/dashboard') ou useRouter().push('/dashboard')
  } catch (error: unknown) {
    console.error('Erro no login:', error)
    if (error instanceof Error) {
      alert('Login falhou: ' + error.message)
    } else {
      alert('Login falhou: Erro desconhecido')
    }
  }
}
</script>