import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  courseSidebar: [
    {
      type: 'category',
      label: 'Welcome',
      collapsed: false,
      items: [
        'index',
        'getting-started',
      ],
    },
    {
      type: 'category',
      label: '01 · Data Loading',
      collapsed: false,
      link: {
        type: 'doc',
        id: 'data-loading/index',
      },
      items: [
        {
          type: 'category',
          label: 'Core Patterns',
          collapsed: false,
          items: [
            'data-loading/batch-loading',
            'data-loading/auto-loader',
            'data-loading/micro-batches',
            'data-loading/streaming',
            'data-loading/change-data-capture',
            'data-loading/merge-scd',
          ],
        },
        {
          type: 'category',
          label: 'Extended Sources',
          items: [
            'data-loading/message-queues',
            'data-loading/change-data-feed',
            'data-loading/jdbc-federation',
            'data-loading/zerobus',
            'data-loading/lakeflow-connect',
            'data-loading/custom-sources',
            'data-loading/delta-sharing',
          ],
        },
        {
          type: 'category',
          label: 'Reference',
          items: [
            'data-loading/datasets',
          ],
        },
      ],
    },
    {
      type: 'category',
      label: '02 · SCD',      link: {
        type: 'doc',
        id: 'scd/index',
      },
      items: [
        {
          type: 'category',
          label: 'Types',
          collapsed: false,
          items: [
            'scd/scd-type-0',
            'scd/scd-type-1',
            'scd/scd-type-2',
            'scd/scd-type-3',
          ],
        },
        {
          type: 'category',
          label: 'Advanced',
          items: [
            'scd/early-arriving-facts',
          ],
        },
      ],
    },
  ],
};

export default sidebars;
