export const getToken = () => localStorage.getItem('token')
export const getUserId = () => localStorage.getItem('userId')
export const getUserRole = () => localStorage.getItem('role')

export const setAuth = (token, user) => {
  localStorage.setItem('token', token)
  localStorage.setItem('userId', user.id)
  localStorage.setItem('role', user.role)
}

export const clearAuth = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('userId')
  localStorage.removeItem('role')
}
