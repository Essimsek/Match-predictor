import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/fixtures')({
  component: FixturePage,
})

function FixturePage() {
  return <div>Hello "/fixtures"!</div>
}
