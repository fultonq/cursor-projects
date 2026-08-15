export function required<T>(value: T | null | undefined, message = 'required'): T {
  if (value === null || value === undefined || value === '') {
    throw new Error(message);
  }
  return value;
}
