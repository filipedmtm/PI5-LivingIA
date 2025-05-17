<template>
  <div class="min-h-screen bg-gray-100 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8 bg-white p-8 rounded-lg shadow-lg">
      <div>
        <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
          Entrar na sua conta
        </h2>
        <p class="mt-2 text-center text-sm text-gray-600">
          Não tem uma conta?
          <router-link to="/register" class="font-medium text-teal-700 hover:text-teal-800">
            Cadastre-se
          </router-link>
        </p>
      </div>
      <form class="mt-8 space-y-6" @submit.prevent="handleLogin">
        <div class="rounded-md shadow-sm -space-y-px">
          <div>
            <label for="email" class="sr-only">Email</label>
            <input
              id="email"
              v-model="form.email"
              name="email"
              type="email"
              required
              class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-teal-700 focus:border-teal-700 focus:z-10 sm:text-sm"
              placeholder="Email"
            />
          </div>
          <div>
            <label for="password" class="sr-only">Senha</label>
            <input
              id="password"
              v-model="form.password"
              name="password"
              type="password"
              required
              class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-teal-700 focus:border-teal-700 focus:z-10 sm:text-sm"
              placeholder="Senha"
            />
          </div>
        </div>
        <div>
          <button
            type="submit"
            class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-teal-700 hover:bg-teal-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-teal-700"
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

const router = useRouter()
const form = ref({
  email: '',
  password: '',
})

async function handleLogin() {
  try {
    await login(form.value.email, form.value.password)
    router.push('/dashboard')
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

<!-- /*
  VERSÃO ALTERNATIVA USANDO useAuth
  =================================
  
  <template>
    <div class="min-h-screen bg-gray-100 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div class="max-w-md w-full space-y-8 bg-white p-8 rounded-lg shadow-lg">
        <div>
          <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Entrar na sua conta
          </h2>
        </div>
        
        // Formulário usando o composable useAuth
        <form class="mt-8 space-y-6" @submit.prevent="handleSubmit">
          <div class="rounded-md shadow-sm -space-y-px">
            <div>
              <label for="email" class="sr-only">Email</label>
              // v-model="form.email" - Vincula ao estado do composable
              <input
                id="email"
                v-model="form.email"
                name="email"
                type="email"
                required
                class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-teal-700 focus:border-teal-700 focus:z-10 sm:text-sm"
                placeholder="Email"
              />
            </div>
            <div>
              <label for="password" class="sr-only">Senha</label>
              // v-model="form.password" - Vincula ao estado do composable
              <input
                id="password"
                v-model="form.password"
                name="password"
                type="password"
                required
                class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-teal-700 focus:border-teal-700 focus:z-10 sm:text-sm"
                placeholder="Senha"
              />
            </div>
          </div>
          <div>
            <button
              type="submit"
              class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-teal-700 hover:bg-teal-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-teal-700"
            >
              Entrar
            </button>
          </div>
        </form>
      </div>
    </div>
  </template>

  <script setup lang="ts">
  // 1. Importa o composable useAuth que contém a lógica de autenticação
  import { useAuth } from '@/composables/useAuth'
  import { useRouter } from 'vue-router'

  // 2. Inicializa o router para navegação
  const router = useRouter()

  // 3. Desestrutura o que precisamos do composable:
  // - form: estado reativo com email e password
  // - register: função para fazer o login
  const { form, register } = useAuth()

  // 4. Função que lida com o submit do formulário
  const handleSubmit = async () => {
    // 5. Chama a função register do composable
    const success = await register()
    
    if (success) {
      // 6. Se o login for bem sucedido, redireciona para o dashboard
      router.push('/dashboard')
    } else {
      // 7. Se houver erro, loga no console
      console.log('Erro no login')
    }
  }
  </script>
*/ -->
