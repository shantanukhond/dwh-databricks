import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const config: Config = {
  title: 'DWH on Databricks',
  tagline: 'Learn data warehousing — one video, one notebook, one lesson at a time',
  favicon: 'img/favicon.svg',

  // Custom domain → serve from root
  url: 'https://dwh.shantanukhond.me',
  baseUrl: '/',

  organizationName: 'shantanukhond',
  projectName: 'dwh-databricks',
  deploymentBranch: 'gh-pages',
  trailingSlash: false,

  onBrokenLinks: 'throw',
  markdown: {
    format: 'mdx',
    mermaid: true,
    hooks: {
      onBrokenMarkdownLinks: 'throw',
    },
  },

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  themes: ['@docusaurus/theme-mermaid'],

  presets: [
    [
      'classic',
      {
        docs: {
          routeBasePath: 'docs',
          sidebarPath: './sidebars.ts',
          editUrl: 'https://github.com/shantanukhond/dwh-databricks/edit/main/',
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    image: 'img/social-card.png',
    colorMode: {
      defaultMode: 'light',
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: 'DWH on Databricks',
      logo: {
        alt: 'DWH on Databricks logo',
        src: 'img/logo.svg',
        href: '/docs',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'courseSidebar',
          position: 'left',
          label: 'Course',
        },
        {
          href: 'https://youtube.com/@shantanukhond',
          position: 'right',
          className: 'header-youtube-link',
          'aria-label': 'YouTube channel',
        },
        {
          href: 'https://github.com/shantanukhond/dwh-databricks',
          position: 'right',
          className: 'header-github-link',
          'aria-label': 'GitHub repository',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Course',
          items: [
            {label: '01 · Data Loading', to: '/docs/data-loading'},
            {label: '02 · SCD', to: '/docs/scd'},
            {label: 'Getting Started', to: '/docs/getting-started'},
          ],
        },
        {
          title: 'Community',
          items: [
            {label: 'YouTube', href: 'https://youtube.com/@shantanukhond'},
            {label: 'GitHub', href: 'https://github.com/shantanukhond/dwh'},
          ],
        },
      ],
      copyright: `DWH on Databricks — a free YouTube course · ${new Date().getFullYear()}`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
      additionalLanguages: ['python', 'sql', 'bash', 'yaml'],
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
