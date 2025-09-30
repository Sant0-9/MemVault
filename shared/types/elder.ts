export interface Elder {
  id: number
  name: string
  date_of_birth?: string
  hometown?: string
  current_location?: string
  phone?: string
  email?: string
  emergency_contact?: string
  photo_url?: string
  bio?: string
  personality_traits?: Record<string, any>
  voice_profile_id?: string
  sample_audios?: string[]
  preferred_language: string
  interview_frequency?: string
  privacy_settings?: Record<string, any>
  created_at: string
  updated_at: string
  last_active_at?: string
  is_active: boolean
  deleted_at?: string
}

export interface CreateElderRequest {
  name: string
  date_of_birth?: string
  hometown?: string
  current_location?: string
  phone?: string
  email?: string
  emergency_contact?: string
  photo_url?: string
  bio?: string
  personality_traits?: Record<string, any>
  preferred_language?: string
  interview_frequency?: string
  privacy_settings?: Record<string, any>
}

export interface UpdateElderRequest extends Partial<CreateElderRequest> {}
