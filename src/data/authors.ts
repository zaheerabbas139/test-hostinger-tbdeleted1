export interface Author {
  name: string;
  bio: string;
  avatar: string;
}

// Bylines and bios copied from pranast.com (blog author boxes)
const authors: Record<string, Author> = {
  'Manasa Nadaduru': {
    name: 'Manasa Nadaduru',
    bio: 'Nadaduru Manasa is a Business & Data Analyst and Dynamics 365 CRM Consultant, improves processes through simple and effective digital solutions.',
    avatar: '/assets/images/manasa-nadaduru_avatar-96x96.jpeg',
  },
  'Satish Kumar Balasundaram': {
    name: 'Satish Kumar Balasundaram',
    bio: 'Satish B is an Azure Solution Architect and Cybersecurity & Compliance Specialist, driving secure cloud and modern workplace transformations across Microsoft 365, DevSecOps, and cloud infrastructure environments.',
    avatar: '/assets/images/satish-kumar-balasundaram_avatar-96x96.jpeg',
  },
};

export function getAuthor(name: string): Author {
  const author = authors[name];
  if (!author) {
    throw new Error(`No author profile for "${name}". Add it to src/data/authors.ts.`);
  }
  return author;
}
