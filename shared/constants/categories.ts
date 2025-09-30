export const MEMORY_CATEGORIES = [
  'early-life',
  'coming-of-age',
  'education-career',
  'love-relationships',
  'historical-events',
  'hobbies-passions',
  'wisdom-reflection',
  'spiritual-philosophical',
] as const

export const CATEGORY_LABELS: Record<string, string> = {
  'early-life': 'Early Life',
  'coming-of-age': 'Coming of Age',
  'education-career': 'Education & Career',
  'love-relationships': 'Love & Relationships',
  'historical-events': 'Historical Events',
  'hobbies-passions': 'Hobbies & Passions',
  'wisdom-reflection': 'Wisdom & Reflection',
  'spiritual-philosophical': 'Spiritual & Philosophical',
}

export const DECADES = [
  '1920s',
  '1930s',
  '1940s',
  '1950s',
  '1960s',
  '1970s',
  '1980s',
  '1990s',
  '2000s',
  '2010s',
  '2020s',
] as const

export const EMOTIONS = [
  'joyful',
  'nostalgic',
  'sad',
  'proud',
  'reflective',
  'grateful',
  'humorous',
  'bittersweet',
] as const
