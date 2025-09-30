export interface Memory {
  id: number
  elder_id: number
  title: string
  transcription: string
  summary?: string
  full_text?: string
  audio_url?: string
  audio_cid?: string
  duration_seconds?: number
  waveform_data?: Record<string, any>
  category?: string
  subcategory?: string
  era?: string
  decade?: string
  location?: string
  date_of_event?: string
  people_mentioned?: string[]
  tags?: string[]
  entities?: Record<string, any>
  sentiment?: string
  emotional_tone?: string
  historical_context?: string
  related_events?: Record<string, any>
  play_count: number
  share_count: number
  favorite_by?: number[]
  is_private: boolean
  is_sensitive: boolean
  content_warnings?: string[]
  transcription_confidence?: number
  audio_quality_score?: number
  recorded_at?: string
  created_at: string
  updated_at: string
}

export interface CreateMemoryRequest {
  elder_id: number
  title: string
  transcription?: string
  audio_url?: string
  category?: string
  era?: string
  location?: string
  date_of_event?: string
  people_mentioned?: string[]
  is_private?: boolean
  is_sensitive?: boolean
}

export interface UpdateMemoryRequest extends Partial<CreateMemoryRequest> {}
