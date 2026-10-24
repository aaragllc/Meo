# SPEC - SEO and audience growth (project rule)

Status: adopted 2026-10-23 (Ravi's directive: "Get SEO right from the
get-go and all the audience growth techniques - industrialize in the
platform. Apply for every new channel as appropriate - project rule.").
This spec is the inventory: what the SEO surface is on each channel,
which growth techniques exist, who owns each one, and when each is set.
The project rule itself - the obligation every NEW channel adapter
carries before its first post - is written in `POLICY.md` (section
"SEO and growth - the project rule") and enforced at onboarding by
section 10 of `templates/channel-adapter.md`.

Operating principle: SEO and growth are set AT PREP, not scrambled at
ship. Every field below that says "at prep" must exist in the piece's
prep or metadata file before ship day; the ship gate
(`tools/socialy_check.py ship`) verifies what is automatable, and the
publisher sets the rest at publish and verifies live.

## 1. SEO by surface

### 1.1 Substack article (the search-indexed long-form surface)

| Field | Rule | Set when |
|---|---|---|
| Display title | Persona voice, untouched by SEO concerns | at prep (Stocky draft) |
| Subtitle | 200 chars max, complete sentences only (the editor truncates silently mid-sentence); plain-language, number-forward phrasing carries search weight | drafted at prep, set at publish |
| SEO title | 60 chars max; plain search phrasing of the topic, keyword early; separate from the display title, subscribers never see it | drafted in the prep file next to the subtitle, set at publish |
| SEO description | 160 chars max (draft at about 155); plain summary carrying the topic's search terms | drafted at prep, set at publish |
| Tags | 3-5 per article, only from the taxonomy in `config.yaml` (`growth.substack_tags`) | chosen at prep, set at publish |
| Slug | Never rename after publish (breaks every link); a clean slug may be set only before first publish | at publish |
| Section | Articles file under the article section (that70sda: "that70sda") | at publish |
| Listen link | Once the episode is live, the article is edited to link it (confirmed caret-insert method only - see OPERATING-LESSONS) | at ship, same day |

Enforcement: subtitle length and SEO lengths are linter rules
(SUBTITLE_LEN, SEO_LEN); presence of the subtitle marker and SEO block
is reported by the ship gate, and an article-prep file (one carrying a
subtitle marker) with no SEO block FAILS the ship gate.

### 1.2 Podcast episode (Substack Podcast section; RSS carries it onward)

| Field | Rule | Set when |
|---|---|---|
| Episode subtitle | Episode-specific summary line, 200 chars max (same editor cap) | at prep, in the metadata file |
| Episode description | A real description - what it covers, key points - never the retired fixed one-liner; ends with the follow line from `config.yaml` (`growth.episode_follow_line`); carries the article link and links to related earlier pieces | at prep, in the metadata file (`DESCRIPTION:` block, `Article:` line) |
| Section | Episodes file under the Podcast section | at publish |
| RSS inheritance | Spotify pulls the feed automatically; Apple Podcasts is claimed under the persona's own account decision (config: `growth.apple_podcasts`) - the listing shows only feed contents | standing |

Enforcement: the ship gate checks episode metadata files for the
follow line and an article link, and for the search clause in any
declared YouTube title (below).

### 1.3 YouTube (the second real search surface)

| Field | Rule | Set when |
|---|---|---|
| Video title | Episode title + " - " + a plain search clause (e.g. "the AI build-out, scored"). Display/article titles keep the persona voice; only the YouTube title carries the clause | declared in the episode metadata file as a `YouTube title:` line at prep, set at upload |
| Description | The episode's overview description (the overview-description gate: no description, no upload); article link inside; backlog/old uploads carry the original publish date as a dated line at the top | at upload |
| Playlist | Assigned to its series playlist from `config.yaml` (`growth.playlists`) | at upload |
| End screen | Subscribe + previous episode | at upload |
| Pinned comment | Posted and pinned by the channel: the article link + the next piece's forward reference | at upload |
| Short | 1 per episode (`growth.shorts_per_episode`), vertical, captions burned in, question-form title, uploaded the same day as the episode video | at ship |

Enforcement: a declared `YouTube title:` line missing the " - " search
clause FAILS the ship gate. Playlist, end screen, pinned comment, and
Short are publish-path steps verified live per POLICY (verify_live).

### 1.4 X - no SEO fields; feed and reply driven

Search indexing does not apply. What applies instead:

- Thread structure: first post is the hook; the Substack link is the
  final post while the account is young (blog-first convention).
- Profile surface: bio carries the persona's search-visible one-liner;
  the intro thread stays pinned.
- Discovery levers: replies in-lane (engagement routine), the next-day
  quote post, Communities placement during test windows - all in
  section 2.

### 1.5 LinkedIn company page - no SEO fields; feed driven

- Every post is dated, carries a crisp overview, and ends with the
  cross-promo footnote block linking all channels (Substack, YouTube,
  Spotify, X) - template in the persona pack.
- The page's own fields (tagline, About) carry the search-visible
  description of the persona; the About ends "Not financial advice."
- Follower milestone (config: `growth.linkedin_follower_milestone`,
  150) unlocks the page newsletter; tracked in the Sunday ledger.
  Connection invites are never used (anonymity wall).

### 1.6 Spotify - monitored only

No direct SEO surface: show and episode metadata are inherited from
the Substack episode fields (1.2) via RSS. The obligation is presence
and correctness checks on the weekly parity audit, never assumed.

## 2. Growth techniques inventory

Owner key: PUB = publishing path (per piece, at ship); ENG = daily
engagement routine; WK = weekly (Sunday) cycle; ONCE = one-time setup,
verified standing thereafter.

| Technique | Owner | Cadence | Configured in | Measured in |
|---|---|---|---|---|
| Substack recommendations (warm list, recommend-first) | PUB | standing; list maintained as warm relationships form | `growth.substack_recommendations` | Sunday ledger (subs attributed) |
| Article tags from the taxonomy | PUB | every article | `growth.substack_tags` | SEO-compliance line |
| Substack Notes - 1 original Note + restacks with comment | ENG | daily | `growth.notes_per_day` | Sunday ledger |
| Episode follow line in every description | PUB | every episode | `growth.episode_follow_line` | ship gate + SEO-compliance line |
| YouTube search-clause titles | PUB | every upload | `growth.youtube_title_search_clause` | ship gate + SEO-compliance line |
| YouTube playlists, end screens, pinned comments | PUB | every upload | `growth.playlists` | parity audit |
| Shorts, 1 per episode | PUB | every episode, same day | `growth.shorts_per_episode` | Sunday ledger |
| X next-day quote post (yesterday's thread + one fresh line, when the theme allows) | ENG | daily | `growth.next_day_quote_post` | Sunday ledger |
| X Communities test (joined communities, link rules respected) | ENG | test window 2026-10-24 to 2026-11-06, review at window end | `growth.x_communities_test` | Sunday ledger; cut or keep at review |
| LinkedIn follower milestone tracking toward newsletter eligibility | WK | weekly | `growth.linkedin_follower_milestone` | Sunday ledger |
| Cross-promo footnote block on every LinkedIn post; cross-links inside every article/episode/thread | PUB | every piece | persona pack template | parity audit |
| Welcome email installed (approved text; verified saved) | ONCE | standing | persona pack files | STATE snapshot |
| Apple Podcasts claim of the RSS listing | ONCE | standing once claimed | `growth.apple_podcasts` | Sunday report until live |
| Content repository regeneration (full-text PDF of all articles) | WK | Sunday cycle | tools/socialy_repository.py | Sunday report |
| Growth ledger with the 4-week cut rule (a lever producing nothing in 4 weeks gets cut) | WK | Sunday report | `growth.growth_ledger_in_sunday_report` | the ledger itself |

## 3. Sunday reporting requirement

The Sunday report (audience one-pager) carries, alongside the
ops-health section:

1. **SEO-compliance line** - of the pieces shipped that week, how many
   carried every automatable field: subtitle within cap, SEO title +
   description set, tags chosen, episode follow line present, YouTube
   search-clause title, playlist + end screen + pinned comment done.
   Source: the week's ship-gate runs and the parity audit. Any miss is
   named with its piece, not averaged away.
2. **Growth ledger** - subscribers/followers by channel with
   attributed sources where the platform shows them, lever by lever
   against section 2, and the 4-week cut rule applied: a lever with
   four straight weeks of nothing is proposed for cutting in the
   report, not silently dropped.

## 4. New channels

The project rule (POLICY.md) applies at onboarding: before a new
channel adapter's first post, its SEO surface is mapped in section 10
of its adapter doc (fields, limits, where set - or N/A with a reason),
its growth actions are wired into the publishing path or the
engagement routine as appropriate to that channel, config entries
exist, ship-gate checks exist where automatable, and its numbers land
in the Sunday growth ledger. Feed-driven channels (the X/LinkedIn
pattern) record what applies instead of SEO fields; a channel with no
growth surface at all records that as its N/A reason and is
monitored-only until that changes.
