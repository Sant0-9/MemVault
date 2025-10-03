import dynamic from 'next/dynamic'
import { Spinner } from '@/components/ui/spinner'

export const LazyTimeline = dynamic(
  () => import('@/components/features/Timeline'),
  {
    loading: () => (
      <div className="flex items-center justify-center py-12">
        <Spinner size="lg" />
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
        <Spinner />
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
        <Spinner />
      </div>
    ),
    ssr: false,
  }
)
