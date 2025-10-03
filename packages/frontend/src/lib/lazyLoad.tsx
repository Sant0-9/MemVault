import dynamic from 'next/dynamic'
import React from 'react'

export const LazyTimeline = dynamic(
  () => import('@/components/features/Timeline'),
  {
    loading: () => (
      <div className="flex items-center justify-center py-12">
        <div className="text-sm text-neutral-400">Loading...</div>
      </div>
    ),
    ssr: false,
  }
)

export const LazyVoiceProfile = dynamic(
  () => import('@/components/features/VoiceProfile'),
  {
    loading: () => (
      <div className="flex items-center justify-center py-8">
        <div className="text-sm text-neutral-400">Loading...</div>
      </div>
    ),
    ssr: false,
  }
)

export const LazyExportMemories = dynamic(
  () => import('@/components/features/ExportMemories'),
  {
    loading: () => (
      <div className="flex items-center justify-center py-8">
        <div className="text-sm text-neutral-400">Loading...</div>
      </div>
    ),
    ssr: false,
  }
)
