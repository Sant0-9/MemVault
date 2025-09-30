export interface ApiResponse<T> {
  success: boolean
  data?: T
  message?: string
  error?: string
  detail?: string
  request_id?: string
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  size: number
  pages: number
}

export interface PaginationParams {
  page?: number
  size?: number
  sort_by?: string
  order?: 'asc' | 'desc'
}

export interface ErrorResponse {
  success: false
  error: string
  detail?: string
  request_id?: string
}
