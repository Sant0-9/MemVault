import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { Card, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-background to-muted">
      <header className="container mx-auto px-4 py-6">
        <div className="flex items-center justify-between">
          <h1 className="text-2xl font-bold">MemoryVault</h1>
          <div className="flex items-center gap-4">
            <Link href="/login">
              <Button variant="ghost">Login</Button>
            </Link>
            <Link href="/register">
              <Button>Get Started</Button>
            </Link>
          </div>
        </div>
      </header>

      <main>
        <section className="container mx-auto px-4 py-20 text-center">
          <h2 className="text-5xl font-bold mb-6">
            Preserve Life Stories for Future Generations
          </h2>
          <p className="text-xl text-muted-foreground mb-8 max-w-2xl mx-auto">
            AI-powered platform to capture, preserve, and share precious family memories.
            Never lose another family story.
          </p>
          <div className="flex items-center justify-center gap-4">
            <Link href="/register">
              <Button size="lg" className="text-lg px-8 py-6">
                Start Preserving Memories
              </Button>
            </Link>
            <Link href="/dashboard">
              <Button size="lg" variant="outline" className="text-lg px-8 py-6">
                View Demo
              </Button>
            </Link>
          </div>

          <div className="mt-12 text-sm text-muted-foreground">
            70% of family stories are lost within two generations. Not anymore.
          </div>
        </section>

        <section className="container mx-auto px-4 py-20">
          <h3 className="text-3xl font-bold text-center mb-12">How It Works</h3>
          <div className="grid md:grid-cols-3 gap-8">
            <Card>
              <CardHeader>
                <div className="text-4xl mb-4">AI</div>
                <CardTitle>Record Memories</CardTitle>
                <CardDescription>
                  AI interviewer asks thoughtful questions to capture life stories naturally
                </CardDescription>
              </CardHeader>
            </Card>

            <Card>
              <CardHeader>
                <div className="text-4xl mb-4">Enhance</div>
                <CardTitle>AI Enhancement</CardTitle>
                <CardDescription>
                  Automatic transcription, categorization, and enrichment with historical context
                </CardDescription>
              </CardHeader>
            </Card>

            <Card>
              <CardHeader>
                <div className="text-4xl mb-4">Forever</div>
                <CardTitle>Preserve Forever</CardTitle>
                <CardDescription>
                  Stored on IPFS - memories are permanent and owned by your family
                </CardDescription>
              </CardHeader>
            </Card>
          </div>
        </section>

        <section className="container mx-auto px-4 py-20">
          <h3 className="text-3xl font-bold text-center mb-12">Advanced Features</h3>
          <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
            <Card>
              <CardHeader>
                <CardTitle>Voice Cloning</CardTitle>
                <CardDescription>
                  Clone elder voices to create new AI-generated messages and memories
                </CardDescription>
              </CardHeader>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Interactive Timeline</CardTitle>
                <CardDescription>
                  Visualize memories across decades, eras, and life stages
                </CardDescription>
              </CardHeader>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Smart Search</CardTitle>
                <CardDescription>
                  Find memories instantly with filters for category, emotion, location, and time
                </CardDescription>
              </CardHeader>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Analytics Dashboard</CardTitle>
                <CardDescription>
                  Insights into emotional patterns, content distribution, and memory completeness
                </CardDescription>
              </CardHeader>
            </Card>
          </div>
        </section>

        <section className="container mx-auto px-4 py-20 text-center">
          <h3 className="text-3xl font-bold mb-6">Ready to Preserve Your Family Stories?</h3>
          <p className="text-xl text-muted-foreground mb-8 max-w-2xl mx-auto">
            Join families worldwide who are preserving precious memories for future generations
          </p>
          <Link href="/register">
            <Button size="lg" className="text-lg px-12 py-6">
              Get Started Free
            </Button>
          </Link>
        </section>
      </main>

      <footer className="border-t mt-20">
        <div className="container mx-auto px-4 py-12">
          <div className="grid md:grid-cols-4 gap-8">
            <div>
              <h4 className="font-bold mb-4">MemoryVault</h4>
              <p className="text-sm text-muted-foreground">
                Preserving life stories for future generations
              </p>
            </div>
            <div>
              <h4 className="font-bold mb-4">Product</h4>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li><Link href="/dashboard">Features</Link></li>
                <li><Link href="/dashboard">Demo</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="font-bold mb-4">Company</h4>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li><Link href="https://github.com">GitHub</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="font-bold mb-4">Legal</h4>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li>Privacy Policy</li>
                <li>Terms of Service</li>
              </ul>
            </div>
          </div>
          <div className="mt-12 pt-8 border-t text-center text-sm text-muted-foreground">
            © 2025 MemoryVault. All rights reserved.
          </div>
        </div>
      </footer>
    </div>
  )
}
