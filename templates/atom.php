<?php echo "<?xml" ?> version="1.0" encoding="UTF-8"?>
<feed xml:base="http://photos.movieos.org" xml:lang="en-US" xmlns="http://www.w3.org/2005/Atom">
  <title type="text">Photos for contacts of Tom Insam</title>
  <id><?php echo $guid ?></id>
  <generator version="0.1" uri="http://code.movieos.org/flickrhub/">FlickrHub</generator>

  <?php $photos = user_photos($user, 100); ?>
  <?php $first = $photos[0]; if ($first): ?>
    <updated><?php echo $first->upload_datetime->format(DateTime::ATOM) ?></updated>
  <?php endif ?>

<?php foreach ($photos as $photo): ?>
  <entry>

    <author>
      <name><?php h($photo->fullname) ?></name>
    </author>
    <published><?php echo $photo->upload_datetime->format(DateTime::ATOM) ?></published>
    <updated><?php echo $photo->upload_datetime->format(DateTime::ATOM) ?></updated>
    <id><?php h($guid) ?>/<?php h($photo->id) ?></id>
    <title><?php h($photo->title) ?></title>
    <link href="<?php echo photo_link($photo) ?>" rel="alternate"/>
    <content type="html"><?php h(
        '<p>' . $photo->fullname . ' posted a photo</p>' .
        '<p style="float: left; margin: 0 20px 20px 0;">' .
          '<a href="' . photo_link($photo) . '">' .
            '<img src="' . photo_url($photo, $size) . '">' .
        '</a></p>' .
        '<p>' . $photo->description . "</p>" )
        // (assume photo description is html-safe.)
    ?></content>
  </entry>

<?php endforeach ?>

</feed>
