#!/usr/bin/env python3
import os, glob, sys
sys.path.insert(0, os.path.dirname(__file__))
from gen_og_gm import make_og

BASES = "_tmp_ogsrc/bases"
OUT = "images"

# slug -> (base_file_prefix, title)
M = [
 ("ai-transcriber-meeting-notes-2026", "realistic_photo_of_a_person_ta", "AI Transcriber & Meeting Notes"),
 ("best-ai-coding-assistants-2026", "realistic_photo_of_software_de", "Best AI Coding Assistants in 2026"),
 ("best-ai-note-taking-tools-2026", "realistic_photo_of_handwritten", "Best AI Note-Taking & Knowledge Tools in 2026"),
 ("best-ai-paraphrasing-tools-2026", "realistic_photo_of_a_person_ed", "Best AI Paraphrasing & Rewriting Tools in 2026"),
 ("best-ai-seo-tools-2026", "realistic_photo_of_an_analytic", "6 Best AI SEO Tools to Rank Higher in 2026"),
 ("best-ai-tools-faceless-youtube-2026", "realistic_photo_of_a_camera_an", "Best AI Tools for Faceless YouTube Channels in 2026"),
 ("best-ai-tools-for-email-marketing-2026", "realistic_photo_of_an_inbox_an", "Best AI Tools for Email Marketing in 2026"),
 ("best-ai-tools-for-podcasters-2026", "realistic_photo_of_a_podcast_m", "Best AI Tools for Podcasters in 2026"),
 ("best-ai-tools-for-small-business-2026", "realistic_photo_of_a_small_bus", "Best AI Tools for Small Business in 2026"),
 ("best-ai-tools-for-social-media-managers-2026", "realistic_photo_of_a_social_me", "Best AI Tools for Social Media Managers in 2026"),
 ("best-ai-tools-for-students-2026", "realistic_photo_of_a_student_s", "Best AI Tools for Students in 2026"),
 ("best-ai-tools-for-youtube-creators-2026", "realistic_photo_of_a_youtube_c", "Best AI Tools for YouTube Creators in 2026"),
 ("best-ai-voice-generator-tools-2026", "realistic_photo_of_a_studio_mi", "Best AI Voice Generator Tools in 2026"),
 ("best-free-ai-tools-content-creators-2026", "realistic_photo_of_a_content_c", "Best Free AI Tools for Content Creators in 2026"),
 ("chatgpt-vs-claude-vs-gemini-2026", "realistic_photo_of_three_smart", "ChatGPT vs Claude vs Gemini: Which AI Is Best in 2026?"),
 ("copy-ai-review-2026", "realistic_close_up_photo_of_ha", "Copy.ai Review 2026"),
 ("descript-ai-review-2026", "realistic_photo_of_a_video_edi", "Descript Review 2026"),
 ("elevenlabs-review-2026", "realistic_photo_of_a_professio", "ElevenLabs Review 2026"),
 ("generative-engine-optimization-guide-2026", "realistic_photo_of_a_person_at", "Generative Engine Optimization Guide 2026"),
 ("grammarlygo-review-2026", "realistic_photo_of_a_writing_a", "GrammarlyGo Review 2026"),
 ("hugging-face-new-models-2026", "realistic_photo_of_a_server_ra", "Hugging Face New Models 2026"),
 ("jasper-vs-writesonic", "realistic_photo_of_an_AI_writi", "Jasper vs Writesonic: Which AI Writer Wins in 2026?"),
 ("koalawriter-review-2026", "realistic_photo_of_a_blog_post", "KoalaWriter Review 2026"),
 ("make-com-review-2026", "realistic_photo_of_automation", "Make.com Review 2026"),
 ("notion-ai-review-2026", "realistic_photo_of_a_notes_app", "Notion AI Review 2026"),
 ("open-source-ai-models-2026", "realistic_photo_of_open_source", "Open-Source AI Models 2026"),
 ("perplexity-ai-review-2026", "realistic_photo_of_research_an", "Perplexity AI Review 2026"),
 ("rytr-review-2026", "realistic_photo_of_budget_writ", "Rytr Review 2026"),
 ("writesonic-review-2026", "realistic_photo_of_a_marketer", "Writesonic Review 2026"),
 ("track-brand-visibility-ai-search-2026", "realistic_photo_of_brand_analy", "Track Brand Visibility in AI Search 2026"),
]

files = os.listdir(BASES)
for slug, prefix, title in M:
    matches = [f for f in files if f.startswith(prefix) and f.endswith(".png")]
    if not matches:
        print(f"!! NO BASE for {slug} (prefix {prefix})"); continue
    base = os.path.join(BASES, sorted(matches)[0])
    out = os.path.join(OUT, f"og-{slug}.jpg")
    make_og(base, title, out)
    print(f"OK og-{slug}.jpg  <- {os.path.basename(base)}")
print("DONE")
