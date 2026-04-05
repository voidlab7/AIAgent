// 在 xiaohongshu.com 页面的控制台执行
copy(document.cookie.split('; ').map(c => {
  const [name, ...rest] = c.split('=');
  return {
    name: name,
    value: rest.join('='),
    domain: '.xiaohongshu.com',
    path: '/',
    expires: Date.now()/1000 + 86400*30,
    httpOnly: false,
    secure: true,
    sameSite: 'Lax'
  }
}))