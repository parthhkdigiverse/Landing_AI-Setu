import Header from "@/components/Header";
import Footer from "@/components/Footer";
import { useParams, Link } from "react-router-dom";
import { motion } from "framer-motion";
import { Calendar, User, ArrowLeft } from "lucide-react";
import { useState, useEffect } from "react";
import { fetchBlogPostDetail, BlogPost as BlogPostType } from "@/services/api";
import SEO from "@/components/SEO";

const BlogPost = () => {
  const { postId } = useParams<{ postId: string }>(); // This is actually the slug
  const [post, setPost] = useState<BlogPostType | null>(null);
  const [loading, setLoading] = useState(true);

  const isPreview = typeof window !== 'undefined' ? new URLSearchParams(window.location.search).get('is_preview') === '1' : false;

  useEffect(() => {
    const handleMessage = (event: MessageEvent) => {
      if (event.data && typeof event.data === 'object' && event.data.source === 'django-admin' && event.data.model?.toLowerCase() === 'blogpost') {
        const payload = event.data.payload;
        setPost((prev: any) => ({
          ...prev,
          ...payload
        }));
      }
    };
    window.addEventListener("message", handleMessage);
    return () => window.removeEventListener("message", handleMessage);
  }, []);

  useEffect(() => {
    const loadPost = async () => {
      if (!postId) return;
      setLoading(true);
      const data = await fetchBlogPostDetail(postId);
      setPost(data);
      setLoading(false);
    };
    loadPost();
  }, [postId]);

  if (loading) {
    return (
      <>
        {!isPreview && <Header />}
        <main className="min-h-[60vh] flex items-center justify-center bg-[#F5F6FA]">
          <div className="text-gray-500">Loading article...</div>
        </main>
        {!isPreview && <Footer />}
      </>
    );
  }

  if (!post) {
    return (
      <>
        {!isPreview && <Header />}
        <main className="min-h-[60vh] flex items-center justify-center bg-gradient-to-br from-[#F5F6FA] to-[#E8ECF4]">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{
              duration: 0.5,
              ease: [0.25, 0.46, 0.45, 0.94]
            }}
            className="text-center bg-white/90 backdrop-blur-lg p-8 rounded-2xl shadow-2xl border border-white/20"
          >
            <h1 className="text-3xl font-bold text-[#1F2E4D] mb-4">Post not found</h1>
            <Link to="/blog" className="inline-flex items-center gap-2 text-[#F4B400] font-semibold hover:text-[#E6B800] transition-colors duration-300">
              <ArrowLeft size={20} />
              Back to blog
            </Link>
          </motion.div>
        </main>
        {!isPreview && <Footer />}
      </>
    );
  }

  return (
    <>
      <SEO 
        title={post.seo_title || post.title} 
        description={post.seo_description || post.excerpt}
        keywords={post.seo_keywords}
        ogImage={post.featured_image_url}
        ogType="article"
      />
      {!isPreview && <Header />}
      <main className="bg-gradient-to-br from-[#F5F6FA] via-[#F0F2F9] to-[#E8ECF4] min-h-screen overflow-x-hidden">
        <motion.section
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.8, ease: "easeOut" }}
          className="max-w-6xl mx-auto px-6 py-16"
        >
          {/* Breadcrumb */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{
              delay: 0.2,
              duration: 0.5,
              ease: [0.25, 0.46, 0.45, 0.94]
            }}
            className="mb-8"
          >
            <Link to="/blog" className="inline-flex items-center gap-2 text-[#F4B400] hover:text-[#E6B800] transition-colors duration-300 font-medium">
              <ArrowLeft size={18} />
              Back to Blog
            </Link>
          </motion.div>

          {/* Title */}
          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{
              delay: 0.3,
              duration: 0.6,
              ease: [0.25, 0.46, 0.45, 0.94]
            }}
            className="text-5xl md:text-6xl font-bold text-[#1F2E4D] mb-6 leading-tight"
          >
            {post.title}
          </motion.h1>

          {/* Meta Information */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{
              delay: 0.4,
              duration: 0.5,
              ease: [0.25, 0.46, 0.45, 0.94]
            }}
            className="flex flex-wrap items-center gap-6 mb-8 p-6 bg-white/60 backdrop-blur-sm rounded-2xl shadow-lg border border-white/20"
          >
            <div className="flex items-center gap-2 text-gray-700">
              <User size={18} className="text-[#F4B400]" />
              <span className="font-medium">{post.author}</span>
            </div>
            <div className="flex items-center gap-2 text-gray-600">
              <Calendar size={18} className="text-[#F4B400]" />
              <span>{new Date(post.created_at).toLocaleDateString()}</span>
            </div>
          </motion.div>

          {/* Featured Image and Content Container */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{
              delay: 0.5,
              duration: 0.6,
              ease: [0.25, 0.46, 0.45, 0.94]
            }}
          >
            {/* Featured Image */}
            <div className="relative overflow-hidden rounded-t-3xl shadow-2xl group mb-0">
              <img
                src={post.featured_image_url || "/placeholder.svg"}
                alt={post.title}
                className="w-full h-auto max-h-[500px] object-cover transition-transform duration-500 group-hover:scale-105"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-black/20 via-transparent to-transparent group-hover:from-black/30 transition-all duration-500"></div>
            </div>

            {/* Content */}
            <motion.div
              initial={{ opacity: 0, y: 15 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{
                delay: 0.6,
                duration: 0.5,
                ease: [0.25, 0.46, 0.45, 0.94]
              }}
              className="prose prose-xl max-w-none bg-white/90 backdrop-blur-sm p-8 md:p-12 rounded-b-3xl shadow-2xl border border-white/30 border-t-0 relative z-10"
            >
              <div 
                className="text-gray-800 leading-relaxed mb-6 text-lg font-medium blog-content"
                dangerouslySetInnerHTML={{ __html: post.content }}
              />
            </motion.div>
          </motion.div>

          {/* Bottom Navigation */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{
              delay: 1.0,
              duration: 0.5,
              ease: [0.25, 0.46, 0.45, 0.94]
            }}
            className="mt-16 text-center"
          >
            <Link
              to="/blog"
              className="inline-flex items-center gap-3 bg-gradient-to-r from-[#F4B400] to-[#E6B800] text-white px-8 py-4 rounded-full font-bold hover:from-[#E6B800] hover:to-[#D4A600] transition-all duration-300 shadow-lg hover:shadow-xl transform hover:-translate-y-1"
            >
              <ArrowLeft size={20} />
              Back to All Articles
            </Link>
          </motion.div>
        </motion.section>
      </main>
      {!isPreview && <Footer />}
    </>
  );
};

export default BlogPost;
