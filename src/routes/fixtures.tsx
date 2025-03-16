import { createFileRoute } from '@tanstack/react-router'
import FixturesPage from '../pages/FixturesPage'

export const Route = createFileRoute('/fixtures')({
  component: FixturesPage,
})
