import { useEffect, useState } from "react";
import Header from "@/components/Header";
import Footer from "@/components/Footer";
import { useParams } from "react-router-dom";
import SEO from "@/components/SEO";

const PolicyPage = () => {
  const { slug } = useParams();
  const [data, setData] = useState<any>(null);
  const [livePreview, setLivePreview] = useState<any>(null);

  useEffect(() => {
    if (slug === 'new-policy') {
      setData({
        title: "New Policy",
        description: "Start typing in the admin panel to preview your policy...",
        sections: []
      });
      return;
    }

    fetch(`/api/policies/${slug}/`)
      .then(res => res.json())
      .then(setData);
  }, [slug]);

  useEffect(() => {
    const handleMessage = (event: MessageEvent) => {
      // Validate the source if necessary (e.g., check origin)
      if (event.data && event.data.source === 'django-admin' && event.data.model === 'Policy') {
        const payload = event.data.payload;
        
        if (payload.sections && Array.isArray(payload.sections)) {
            setLivePreview({
                title: payload.title,
                description: payload.description,
                sections: payload.sections.filter((s: any) => !s.DELETE)
            });
        } else {
            // Parse the dynamic inline formset into a proper array
            const parsedSections: any[] = [];
            Object.keys(payload).forEach(key => {
                if (key.startsWith('sections-') && !key.includes('TOTAL_FORMS') && !key.includes('INITIAL_FORMS') && !key.includes('MAX_NUM_FORMS') && !key.includes('MIN_NUM_FORMS')) {
                    const parts = key.split('-');
                    if (parts.length >= 3) {
                        const index = parseInt(parts[1], 10);
                        const fieldName = parts.slice(2).join('-'); // e.g., 'heading' or 'content'
                        
                        if (!parsedSections[index]) {
                            parsedSections[index] = { id: `live-${index}` };
                        }
                        parsedSections[index][fieldName] = payload[key];
                    }
                }
            });
            
            const validSections = parsedSections.filter(s => s && !s.DELETE);

            setLivePreview({
                title: payload.title,
                description: payload.description,
                sections: validSections
            });
        }

        // Optional smooth scrolling
        if (event.data.scrollTarget) {
            const targetElement = document.getElementById(event.data.scrollTarget);
            if(targetElement) {
                targetElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        }
      }
    };

    window.addEventListener('message', handleMessage);
    return () => window.removeEventListener('message', handleMessage);
  }, []);

  const displayData = livePreview || data;

  if (!displayData) return <div className="text-center py-20">Loading...</div>;

  return (
    <>
      <SEO 
        title={displayData.seo_title || displayData.title} 
        description={displayData.seo_description || displayData.description}
        keywords={displayData.seo_keywords}
      />
      <Header />

      <main>
        {/* HERO */}
        <div id="id_title" className="bg-[#1F2E4D] text-white py-16 text-center">
          <h1 className="text-4xl font-bold">{displayData.title}</h1>
        </div>

        {/* CONTENT */}
        <div className="max-w-3xl mx-auto py-12 px-6">

          {/* DESCRIPTION */}
          <p id="id_description" className="text-gray-600 mb-8 whitespace-pre-wrap">
            {displayData.description}
          </p>

          {/* SECTIONS */}
          <div className="space-y-6">
            {displayData.sections && displayData.sections.length > 0 ? (
                displayData.sections.map((sec: any, index: number) => (
                  <div key={sec.id || index} id={`id_sections-${index}-heading`}>
                    <h3 className="font-bold text-lg mb-2">
                      {sec.heading}
                    </h3>
                    <p id={`id_sections-${index}-content`} className="text-gray-600 whitespace-pre-wrap">
                      {sec.content}
                    </p>
                  </div>
                ))
            ) : null}
          </div>

        </div>
      </main>

      <Footer />
    </>
  );
};

export default PolicyPage;