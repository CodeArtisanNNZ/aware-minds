import {describe,it,expect} from 'vitest';
import {renderToStaticMarkup} from 'react-dom/server';
import {AwarenessOrb,Landing} from './extra';
describe('public product experience',()=>{
 it('identifies the orb state accessibly',()=>{const html=renderToStaticMarkup(<AwarenessOrb state="listening"/>);expect(html).toContain('Aware Minds listening');expect(html).toContain('awareness-orb listening')});
 it('labels the demo as a preview and keeps integration keys server-side',()=>{const html=renderToStaticMarkup(<Landing/>);expect(html).toContain('PREVIEW');expect(html).toContain('Your server keeps the secret');expect(html).toContain('Bujhi')});
});
