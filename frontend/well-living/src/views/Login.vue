<template>
  <div class="w-screen min-h-screen bg-orange-100 flex">
    <!-- Lado esquerdo -->
    <div class="w-[714px] h-screen bg-teal-700 relative overflow-hidden">
      <img class="size-62 left-[-20px] top-0 absolute" :src="WellLivingImage" alt="Well Living" />
      <div class="w-[513px] h-40 left-[100px] top-[253px] absolute justify-start text-white text-5xl font-bold font-['Manrope']">
        OLÁ, <br />SEJA BEM-VINDO!
      </div>
      <div class="w-[464px] h-48 left-[100px] top-[418px] absolute justify-start text-white text-3xl font-medium font-['Manrope']">
        Faça login ou cadastre-se para desfrutar do melhor.
      </div>
      <img class="size-[1024px] left-0 top-0 absolute opacity-10" :src="ElementoGrafico" alt="Elemento gráfico" />
    </div>

    <!-- Formulário -->
    <div class="flex flex-col justify-center items-center flex-1">
      <div class="w-80 text-center text-stone-900 text-5xl font-bold font-['Manrope'] mb-6">
        WELL LIVING
      </div>
      <div class="w-96 text-center text-stone-900 text-4xl font-bold font-['Manrope'] mb-2">
        Bem vindo de volta!
      </div>
      <div class="w-96 text-center mb-8">
        <span class="text-stone-900 text-3xl font-light font-['Manrope']">Não tem uma conta? </span>
        <router-link to="/register" class="text-stone-900 text-3xl font-semibold font-['Manrope'] hover:underline">
          Crie uma agora!
        </router-link>
      </div>

      <form class="flex flex-col space-y-8" @submit.prevent="handleLogin">
        <div class="w-96">
          <input
            v-model="form.email"
            type="email"
            required
            class="w-full h-12 border-b border-stone-500 bg-transparent text-stone-900 text-2xl font-normal font-['Manrope'] placeholder-stone-500 focus:outline-none"
            placeholder="Email"
          />
        </div>

        <div class="w-96">
          <input
            v-model="form.password"
            type="password"
            required
            class="w-full h-12 border-b border-stone-500 bg-transparent text-stone-900 text-2xl font-normal font-['Manrope'] placeholder-stone-500 focus:outline-none"
            placeholder="Senha"
          />
        </div>

        <div class="w-80 text-stone-500 text-2xl font-bold font-['Manrope']">
          <a href="#" class="hover:underline">Esqueci minha senha.</a>
        </div>

        <div class="w-96">
          <button
            type="submit"
            class="w-full h-20 bg-teal-700 rounded-3xl text-white text-3xl font-bold font-['Manrope'] hover:bg-teal-800 transition-colors"
          >
            Entrar
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { login } from '../services/auth'
import { useRouter } from 'vue-router'
import WellLivingImage from '../assets/wellLiving.png'
import ElementoGrafico from '../assets/elementoGrafico.png'

const router = useRouter()
const form = ref({
  email: '',
  password: '',
})

async function handleLogin() {
  try {
    const response = await login(form.value.email, form.value.password)
    if (response.success) {
      router.push('/dashboard')
    } else {
      alert('Login falhou: ' + response.message)
    }
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
