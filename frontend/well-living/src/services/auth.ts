import axios from 'axios';

const API_URL = 'http://localhost:5000'; 

export async function login(email: string, password: string) {
  const response = await axios.post(`${API_URL}/auth/login`, { email, password });
  if (response.data.success) {
    return response.data;
  }
  throw new Error(response.data.message || 'Erro ao fazer login');
}

export async function register(name: string, email: string, password: string) {
  const response = await axios.post(`${API_URL}/auth/register`, { name, email, password });
  if (response.data.success) {
    return response.data;
  }
  throw new Error(response.data.message || 'Erro ao cadastrar');
}