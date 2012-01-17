<h1>All contacts</h1>
<?php foreach (user_all_contacts($user) as $contact): ?>

  <p><?php h($contact->fullname) ?> - last upload <?php h($contact->last_upload) ?></p>

  <p>
  <?php foreach (contact_photos($user, $contact, 10) as $photo): ?>
    <a href="<?php echo photo_link($photo) ?>"><img src="<?php echo photo_url($photo, "s") ?>" width="75" height"75"></a>
  <?php endforeach ?>
  </p>

<?php endforeach ?>
