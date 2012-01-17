  <h1>Photo feeds</h1>
  <p>These feeds may contain private photos. Don't share their urls.</p>
  
  <p>All photos by friends/family/contacts:
    <br><a href="<?php echo $feed_url ?>?size=m">small photos</a>
    <br><a href="<?php echo $feed_url ?>?size=r">regular photos</a>
    <br><a href="<?php echo $feed_url ?>?size=z">large photos</a>
  </p>


<h2>Recently changed contacts</h2>  
<?php foreach (user_contacts($user, 10) as $contact): ?>

  <p><?php h($contact->fullname) ?> - last upload <?php h($contact->last_upload) ?></p>

  <p>
  <?php foreach (contact_photos($user, $contact, 10) as $photo): ?>
    <a href="<?php echo photo_link($photo) ?>"><img src="<?php echo photo_url($photo, "s") ?>" width="75" height"75"></a>
  <?php endforeach ?>
  </p>

<?php endforeach ?>
