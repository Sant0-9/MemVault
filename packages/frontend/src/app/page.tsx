'use client'

import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { Card, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-background to-primary/5">
      <header className="container mx-auto px-4 py-6 backdrop-blur-sm sticky top-0 z-50 border-b border-border/40">
        <div className="flex items-center justify-between">
          <h1 className="text-2xl font-bold bg-gradient-to-r from-primary to-primary/60 bg-clip-text text-transparent">
            MemoryVault
          </h1>
          <div className="flex items-center gap-4">
            <Link href="/login">
              <Button variant="ghost" className="hover:scale-105 transition-transform">
                Login
              </Button>
            </Link>
            <Link href="/register">
              <Button className="hover:scale-105 transition-transform">
                Get Started
              </Button>
            </Link>
          </div>
        </div>
      </header>

      <main>
        <section className="container mx-auto px-4 py-32 text-center">
          <div className="animate-in fade-in slide-in-from-bottom-4 duration-1000">
            <h2 className="text-6xl md:text-7xl font-bold mb-6 bg-gradient-to-r from-foreground to-foreground/70 bg-clip-text text-transparent">
              Preserve Life Stories<br />for Future Generations
            </h2>
          </div>
          <p className="text-xl text-muted-foreground mb-12 max-w-2xl mx-auto animate-in fade-in slide-in-from-bottom-4 duration-1000 delay-150">
            AI-powered platform to capture, preserve, and share precious family memories.
            Never lose another family story.
          </p>
          <div className="animate-in fade-in slide-in-from-bottom-4 duration-1000 delay-300">
            <Link href="/register">
              <Button size="lg" className="text-lg px-12 py-6 hover:scale-105 transition-all shadow-lg hover:shadow-xl">
                Start Preserving Memories
              </Button>
            </Link>
          </div>

          <div className="mt-16 text-sm text-muted-foreground animate-in fade-in duration-1000 delay-500">
            70% of family stories are lost within two generations. Not anymore.
          </div>
        </section>

        <section className="container mx-auto px-4 py-24">
          <h3 className="text-4xl font-bold text-center mb-16 animate-in fade-in duration-700">
            How It Works
          </h3>
          <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
            <Card className="border-2 hover:border-primary/50 transition-all duration-300 hover:shadow-lg hover:-translate-y-1 group">
              <CardHeader className="space-y-4">
                <div className="text-5xl font-bold text-primary/20 group-hover:text-primary/40 transition-colors">
                  01
                </div>
                <CardTitle className="text-xl">Record Memories</CardTitle>
                <CardDescription className="text-base">
                  AI interviewer asks thoughtful questions to capture life stories naturally
                </CardDescription>
              </CardHeader>
            </Card>

            <Card className="border-2 hover:border-primary/50 transition-all duration-300 hover:shadow-lg hover:-translate-y-1 group">
              <CardHeader className="space-y-4">
                <div className="text-5xl font-bold text-primary/20 group-hover:text-primary/40 transition-colors">
                  02
                </div>
                <CardTitle className="text-xl">AI Enhancement</CardTitle>
                <CardDescription className="text-base">
                  Automatic transcription, categorization, and enrichment with historical context
                </CardDescription>
              </CardHeader>
            </Card>

            <Card className="border-2 hover:border-primary/50 transition-all duration-300 hover:shadow-lg hover:-translate-y-1 group">
              <CardHeader className="space-y-4">
                <div className="text-5xl font-bold text-primary/20 group-hover:text-primary/40 transition-colors">
                  03
                </div>
                <CardTitle className="text-xl">Preserve Forever</CardTitle>
                <CardDescription className="text-base">
                  Stored on IPFS - memories are permanent and owned by your family
                </CardDescription>
              </CardHeader>
            </Card>
          </div>
        </section>

        <section className="container mx-auto px-4 py-24 bg-muted/30">
          <h3 className="text-4xl font-bold text-center mb-16">
            Powerful Features
          </h3>
          <div className="grid md:grid-cols-2 gap-6 max-w-5xl mx-auto">
            <Card className="group hover:shadow-xl transition-all duration-300 hover:-translate-y-1 border-2 hover:border-primary/50">
              <CardHeader className="space-y-2">
                <CardTitle className="text-lg group-hover:text-primary transition-colors">
                  Voice Cloning
                </CardTitle>
                <CardDescription>
                  Clone elder voices to create new AI-generated messages and memories
                </CardDescription>
              </CardHeader>
            </Card>

            <Card className="group hover:shadow-xl transition-all duration-300 hover:-translate-y-1 border-2 hover:border-primary/50">
              <CardHeader className="space-y-2">
                <CardTitle className="text-lg group-hover:text-primary transition-colors">
                  Interactive Timeline
                </CardTitle>
                <CardDescription>
                  Visualize memories across decades, eras, and life stages
                </CardDescription>
              </CardHeader>
            </Card>

            <Card className="group hover:shadow-xl transition-all duration-300 hover:-translate-y-1 border-2 hover:border-primary/50">
              <CardHeader className="space-y-2">
                <CardTitle className="text-lg group-hover:text-primary transition-colors">
                  Smart Search
                </CardTitle>
                <CardDescription>
                  Find memories instantly with filters for category, emotion, location, and time
                </CardDescription>
              </CardHeader>
            </Card>

            <Card className="group hover:shadow-xl transition-all duration-300 hover:-translate-y-1 border-2 hover:border-primary/50">
              <CardHeader className="space-y-2">
                <CardTitle className="text-lg group-hover:text-primary transition-colors">
                  Analytics Dashboard
                </CardTitle>
                <CardDescription>
                  Insights into emotional patterns, content distribution, and memory completeness
                </CardDescription>
              </CardHeader>
            </Card>
          </div>
        </section>

        <section className="container mx-auto px-4 py-32 text-center">
          <div className="max-w-3xl mx-auto space-y-8">
            <h3 className="text-4xl md:text-5xl font-bold">
              Ready to Preserve Your Family Stories?
            </h3>
            <p className="text-xl text-muted-foreground">
              Join families worldwide who are preserving precious memories for future generations
            </p>
            <Link href="/register">
              <Button size="lg" className="text-lg px-16 py-7 hover:scale-105 transition-all shadow-xl hover:shadow-2xl">
                Get Started Free
              </Button>
            </Link>
          </div>
        </section>
      </main>

      <footer className="border-t bg-muted/20">
        <div className="container mx-auto px-4 py-16">
          <div className="grid md:grid-cols-4 gap-12">
            <div className="space-y-4">
              <h4 className="font-bold text-lg bg-gradient-to-r from-primary to-primary/60 bg-clip-text text-transparent">
                MemoryVault
              </h4>
              <p className="text-sm text-muted-foreground leading-relaxed">
                Preserving life stories for future generations
              </p>
            </div>
            <div className="space-y-3">
              <h4 className="font-semibold">Product</h4>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li>
                  <Link href="/dashboard" className="hover:text-primary transition-colors">
                    Features
                  </Link>
                </li>
              </ul>
            </div>
            <div className="space-y-3">
              <h4 className="font-semibold">Company</h4>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li>
                  <Link href="https://github.com" className="hover:text-primary transition-colors">
                    GitHub
                  </Link>
                </li>
              </ul>
            </div>
            <div className="space-y-3">
              <h4 className="font-semibold">Legal</h4>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li className="hover:text-primary transition-colors cursor-pointer">Privacy Policy</li>
                <li className="hover:text-primary transition-colors cursor-pointer">Terms of Service</li>
              </ul>
            </div>
          </div>
          <div className="mt-16 pt-8 border-t text-center text-sm text-muted-foreground">
            © 2025 MemoryVault. All rights reserved.
          </div>
        </div>
      </footer>
    </div>
  )
}
