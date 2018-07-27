set +x
FORUM=${1-562}
topics --where "forum_id = ${FORUM}" --output topics-${FORUM}
topic_first_posts --where "T.forum_id = ${FORUM}" --output topic_first_post-${FORUM}
topic_last_posts --where "T.forum_id = ${FORUM}" --output topic_last_post-${FORUM}
posts --where "forum_id = ${FORUM}" --output posts-${FORUM}
post_texts --where "forum_id = ${FORUM}" --output post_texts-${FORUM}
attachments --where "T.forum_id = ${FORUM}" --output attachments-${FORUM}
cat <<EOF > remove-prev-${FORUM}.sql
DELETE FROM bb_topics WHERE forum_id=${FORUM} ;
DELETE P, T FROM bb_posts AS P, bb_posts_text as T  WHERE P.forum_id=${FORUM} AND P.post_id = T.post_id ;
EOF
cat remove-prev-${FORUM}.sql posts-${FORUM}.sql post_texts-${FORUM}.sql topics-${FORUM}.sql topic_first_post-${FORUM}.sql topic_last_post-${FORUM}.sql attachments-${FORUM}.sql > in_forum-${FORUM}.sql
rm remove-prev-${FORUM}.sql posts-${FORUM}.sql post_texts-${FORUM}.sql topics-${FORUM}.sql topic_first_post-${FORUM}.sql topic_last_post-${FORUM}.sql attachments-${FORUM}.sql




