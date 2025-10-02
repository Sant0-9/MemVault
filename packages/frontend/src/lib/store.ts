import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface User {
  id: number
  email: string
  name: string
}

interface AuthState {
  user: User | null
  accessToken: string | null
  setAuth: (user: User, accessToken: string) => void
  logout: () => void
  isAuthenticated: () => boolean
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      accessToken: null,
      setAuth: (user, accessToken) => {
        localStorage.setItem('access_token', accessToken)
        set({ user, accessToken })
      },
      logout: () => {
        localStorage.removeItem('access_token')
        set({ user: null, accessToken: null })
      },
      isAuthenticated: () => !!get().accessToken,
    }),
    {
      name: 'auth-storage',
    }
  )
)
