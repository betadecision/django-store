export class ApiError extends Error {
  status: number
  details: unknown

  constructor(message: string, status: number, details: unknown) {
    super(message)
    this.name = 'ApiError'
    this.status = status
    this.details = details
  }
}

export async function fetchJson<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(path, {
    ...init,
    headers: {
      Accept: 'application/json',
      ...init?.headers,
    },
  })

  if (!response.ok) {
    let details: unknown = null

    try {
      details = await response.json()
    } catch {
      details = await response.text()
    }

    throw new ApiError('Request failed', response.status, details)
  }

  return response.json() as Promise<T>
}
