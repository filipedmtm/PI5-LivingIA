<template>
  <div class="flex flex-col md:flex-row min-h-screen w-full bg-orange-100 relative overflow-hidden">
    <!-- Lado esquerdo -->
    <div class="flex flex-col justify-center items-center md:w-1/2 w-full bg-teal-700 relative p-8">
      <img class="size-62 left-[-20px] top-0 absolute" :src="WellLivingImage" alt="Well Living" />
      <div class="text-white text-4xl md:text-5xl font-bold font-['Manrope'] text-center mb-4">
        OLÁ, <br />SEJA BEM-VINDO!
      </div>
      <div class="text-white text-2xl md:text-3xl font-medium font-['Manrope'] text-center mb-8">
        Faça login ou cadastre-se para desfrutar do melhor.
      </div>
      <router-link to="/login" class="cursor-pointer">
        <div class="bg-orange-100 rounded-3xl py-4 px-8 text-stone-900 text-2xl md:text-3xl font-bold font-['Manrope'] hover:bg-orange-200 transition">
          Login
        </div>
      </router-link>
    </div>

    <!-- Elemento gráfico grande -->
    <img class="absolute opacity-10 w-[500px] md:w-[800px] lg:w-[1024px] top-10 left-0" :src="ElementoGrafico" alt="Elemento gráfico" />

    <!-- Formulário -->
    <div class="flex flex-col justify-center items-center md:w-1/2 w-full p-8 relative z-10">
      <div class="text-center text-stone-900 text-3xl md:text-4xl font-bold font-['Manrope'] mb-6">
        WELL LIVING
      </div>
      <div class="text-center text-stone-900 text-3xl md:text-4xl font-bold font-['Manrope'] mb-2">
        Bem vindo!
      </div>
      <div class="text-center text-stone-900 text-xl md:text-2xl font-light font-['Manrope'] mb-8">
        Preencha com suas informações:
      </div>

      <form class="space-y-6 w-full max-w-md" @submit.prevent="handleRegister">
        <input
          id="name"
          v-model="form.name"
          name="name"
          type="text"
          required
          class="w-full border-b border-stone-500 bg-transparent text-stone-900 text-xl md:text-2xl font-normal font-['Manrope'] placeholder-stone-500 focus:outline-none py-2"
          placeholder="Nome completo"
        />

        <input
          id="email"
          v-model="form.email"
          name="email"
          type="email"
          required
          class="w-full border-b border-stone-500 bg-transparent text-stone-900 text-xl md:text-2xl font-normal font-['Manrope'] placeholder-stone-500 focus:outline-none py-2"
          placeholder="Email"
        />

        <input
          id="password"
          v-model="form.password"
          name="password"
          type="password"
          required
          class="w-full border-b border-stone-500 bg-transparent text-stone-900 text-xl md:text-2xl font-normal font-['Manrope'] placeholder-stone-500 focus:outline-none py-2"
          placeholder="Senha"
        />

        <input
          id="confirmPassword"
          v-model="form.confirmPassword"
          name="confirmPassword"
          type="password"
          required
          class="w-full border-b border-stone-500 bg-transparent text-stone-900 text-xl md:text-2xl font-normal font-['Manrope'] placeholder-stone-500 focus:outline-none py-2"
          placeholder="Confirmar senha"
        />

        <button
          type="submit"
          class="w-full bg-teal-700 rounded-3xl text-white text-xl md:text-2xl font-bold font-['Manrope'] py-4 hover:bg-teal-800 transition"
        >
          Cadastrar
        </button>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { register } from '../services/auth'
import WellLivingImage from '../assets/wellLiving.png'
import ElementoGrafico from '../assets/elementoGrafico.png'

const router = useRouter()
const form = ref({
  name: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const handleRegister = async () => {
  if (form.value.password !== form.value.confirmPassword) {
    alert('As senhas não coincidem')
    return
  }

  try {
    const response = await register(form.value.name, form.value.email, form.value.password)

    if (response.success) {
      router.push('/dashboard')
    } else {
      alert('Cadastro falhou: ' + response.message)
    }
  } catch (error: unknown) {
    console.error('Registration failed:', error)
    if (error instanceof Error) {
      alert('Erro ao realizar cadastro: ' + error.message)
    } else {
      alert('Erro ao realizar cadastro. Tente novamente.')
    }
  }
}
</script>
