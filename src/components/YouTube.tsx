import type {ReactNode} from 'react';

type YouTubeProps = {
  id: string;
  title: string;
};

export default function YouTube({id, title}: YouTubeProps): ReactNode {
  return (
    <div className="youtube-embed">
      <iframe
        src={`https://www.youtube.com/embed/${id}`}
        title={title}
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
        referrerPolicy="strict-origin-when-cross-origin"
        allowFullScreen
      />
    </div>
  );
}
