<div style="float: left; width: 600px">

  <h1>Photo feeds</h1>
  <p>These feeds may contain private photos. Don't share their urls.</p>
  
  <p>All photos by friends/family/contacts:
    <br><a href="<?php echo $feed_url ?>?size=m">small photos</a>
    <br><a href="<?php echo $feed_url ?>?size=r">regular photos</a>
    <br><a href="<?php echo $feed_url ?>?size=z">large photos</a>
  </p>

</div>

<div style="float: left; width: 200px">
  <h2>recent uploads:</h2>
  <?php foreach (user_photos($user, 10) as $photo): ?>
    <p><?php h($photo->title) ?> by <?php h($photo->fullname) ?></p>
    <p>uploaded <?php h($photo->date_upload) ?></p>
    <a href="<?php echo photo_link($photo) ?>"><img src="<?php echo photo_url($photo, "s") ?>" width="75" height"75"></a>
  <?php endforeach ?>
</div>
