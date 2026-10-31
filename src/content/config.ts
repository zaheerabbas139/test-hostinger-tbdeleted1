import { defineCollection, z } from 'astro:content';

/**
 * Standard Static Pages Schema
 * Used for Home, About, Services, BridgeAD, FAQ, Contact, Legal
 */
const pagesCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string().optional(),
    slug: z.string().optional(),
    date: z.string().optional(),
    modified: z.string().optional(),
    featured_image: z.string().optional(),
    nav_order: z.number().optional(),
  }),
});

/**
 * Blog Articles & Insights Schema
 * Used for technical articles and thought leadership
 */
const blogCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string().optional(),
    slug: z.string().optional(),
    date: z.string(),
    modified: z.string().optional(),
    category: z.enum(['Digital Transformation', 'Cyber Security']),
    featured_image: z.string(),
    featured_image_alt: z.string().optional(),
    author: z.string().default('Prana Solutions Tech'),
    draft: z.boolean().default(false),
  }),
});

/**
 * Client Case Studies Schema
 * Used for in-depth client outcomes and enterprise engagements
 */
const caseStudiesCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    client: z.string(),
    industry: z.string(),
    summary: z.string(),
    slug: z.string().optional(),
    challenge: z.string().optional(),
    solution: z.string().optional(),
    outcome: z.string().optional(),
    featured_image: z.string().optional(),
    date: z.string().optional(),
  }),
});

export const collections = {
  pages: pagesCollection,
  blog: blogCollection,
  'case-studies': caseStudiesCollection,
};
