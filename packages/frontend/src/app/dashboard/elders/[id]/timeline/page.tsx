'use client'

import { useParams } from 'next/navigation'
import Link from 'next/link'
import Timeline from '@/components/features/Timeline'

export default function TimelinePage() {
  const params = useParams()
  const elderId = parseInt(params.id as string)

  return (
    <div className="min-h-screen bg-background">
      <header className="border-b">
        <div className="container mx-auto px-4 py-4">
          <Link
            href={`/dashboard/elders/${elderId}`}
            className="text-sm text-muted-foreground hover:text-foreground"
          >
            ← Back to Elder Profile
          </Link>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8 max-w-6xl">
        <Timeline elderId={elderId} />
      </main>
    </div>
  )
}
