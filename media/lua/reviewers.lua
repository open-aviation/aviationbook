-- Normalize reviewer/reviewers metadata for the HTML title block.
function Meta(meta)
  local reviewers = meta.reviewers or meta.reviewer
  if reviewers == nil then
    return meta
  end

  if pandoc.utils.type(reviewers) ~= "List" then
    reviewers = pandoc.MetaList({ reviewers })
  end

  meta.reviewers = reviewers
  meta.reviewer = nil
  meta["reviewers-label"] = pandoc.MetaString(
    #reviewers == 1 and "Reviewer" or "Reviewers"
  )
  return meta
end
