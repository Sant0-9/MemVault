'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { useAuthStore } from '@/lib/store'

export default function Home() {
  const router = useRouter()
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated())

  useEffect(() => {
    if (isAuthenticated) {
      router.push('/dashboard')
    }
  }, [isAuthenticated, router])

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-8">
      <div className="max-w-5xl w-full items-center justify-between text-center space-y-8">
        <div className="space-y-4">
          <h1 className="text-6xl font-bold">MemoryVault</h1>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            Preserve precious life stories and memories of your loved ones with AI-powered interviews and permanent storage
          </p>
        </div>

        <div className="flex gap-4 justify-center">
          <Button asChild size="lg">
            <Link href="/register">Get Started</Link>
          </Button>
          <Button asChild variant="outline" size="lg">
            <Link href="/login">Sign In</Link>
          </Button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-16 text-left">
          <div className="space-y-2">
            <h3 className="text-lg font-semibold">AI Interviewer</h3>
            <p className="text-sm text-muted-foreground">
              Thoughtful AI asks the right questions to capture meaningful memories
            </p>
          </div>
          <div className="space-y-2">
            <h3 className="text-lg font-semibold">Audio Transcription</h3>
            <p className="text-sm text-muted-foreground">
              Automatic transcription and enrichment with AI-generated tags
            </p>
          </div>
          <div className="space-y-2">
            <h3 className="text-lg font-semibold">Permanent Storage</h3>
            <p className="text-sm text-muted-foreground">
              Decentralized IPFS storage ensures memories last forever
            </p>
          </div>
        </div>
      </div>
    </main>
  )
}
