import axios from 'axios';

const API_URL = 'http://localhost:5000';

export async function login(email: string, password: string) {
  try {
    const response = await axios.post(`${API_URL}/auth/login`, { email, password });
    return response.data;
  } catch (error: any) {
    if (axios.isAxiosError(error) && error.response) {
      throw new Error(error.response.data.message || 'Erro ao fazer login');
    }
    throw new Error('Erro inesperado ao fazer login');
  }
}

export async function register(name: string, email: string, password: string) {
  try {
    const response = await axios.post(`${API_URL}/auth/register`, { name, email, password });
    return response.data;
  } catch (error: any) {
    if (axios.isAxiosError(error) && error.response) {
      throw new Error(error.response.data.message || 'Erro ao cadastrar');
    }
    throw new Error('Erro inesperado ao cadastrar');
  }
}
