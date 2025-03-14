import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/standings')({
  component: StandingsPage,
})

function StandingsPage() {
  return <div>Hello "/standings"!</div>
}
