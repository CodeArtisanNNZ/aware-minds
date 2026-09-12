import {test,expect} from '@playwright/test';
const sizes:[[number,number],...[number,number][]]=[[1920,1080],[1440,900],[1366,768],[1024,768],[768,1024],[430,932],[390,844],[360,800]];
for(const [width,height] of sizes){
 test(`public layout ${width}x${height}`,async({page})=>{
  await page.setViewportSize({width,height});await page.goto('/');
  await expect(page.getByRole('heading',{name:/One intelligence/})).toBeVisible();
  expect(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth+1)).toBe(true);
  await page.screenshot({path:`screenshots/landing-${width}x${height}.png`,fullPage:true});
  await page.goto('/login');
  await expect(page.getByRole('heading',{name:'Sign in to your space'})).toBeVisible();
  expect(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth+1)).toBe(true);
 });
}
test('registration and mobile workspace navigation',async({page})=>{
 await page.setViewportSize({width:390,height:844});await page.goto('/register');
 await page.getByLabel('Email').fill(`e2e-${Date.now()}@test.invalid`);
 await page.getByLabel('Password').fill('correct-horse-battery-123');
 await page.getByRole('button',{name:'Create account'}).click();
 await expect(page.getByRole('heading',{name:'Where should we begin?'})).toBeVisible();
 await page.getByRole('button',{name:'Open menu'}).click();
 await page.getByRole('button',{name:'Library'}).click();
 await expect(page.getByRole('heading',{name:'Library'})).toBeVisible();
 expect(await page.evaluate(()=>document.documentElement.scrollWidth<=window.innerWidth+1)).toBe(true);
 await page.screenshot({path:'screenshots/mobile-library.png'});
});
