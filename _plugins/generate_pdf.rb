require 'fileutils'

Jekyll::Hooks.register :site, :post_write do |site|
  cv_path = File.join(site.source, 'cv.md')
  pdf_path = File.join(site.source, 'assets', 'pdf', 'AnnaRobakowskaCV.pdf')
  site_pdf_path = File.join(site.dest, 'assets', 'pdf', 'AnnaRobakowskaCV.pdf')
  template_path = File.join(site.source, 'assets', 'templates', 'template.html')
  style_css_path = File.join(site.source, 'assets', 'css', 'style.css')
  print_css_path = File.join(site.source, 'assets', 'css', 'print-style.css')

  need_generate = !File.exist?(pdf_path) || File.mtime(cv_path) > File.mtime(pdf_path) || !File.exist?(site_pdf_path)

  if need_generate && !@pdf_running
    @pdf_running = true
    begin
      pandoc_dir = "C:\\Users\\annam\\AppData\\Local\\Pandoc"
      ENV['PATH'] = "#{pandoc_dir};#{ENV['PATH']}" unless ENV['PATH'].include?(pandoc_dir)

      cmd = "pandoc \"#{cv_path}\" -o \"#{pdf_path}\" --template=\"#{template_path}\" --css=\"#{style_css_path}\" --css=\"#{print_css_path}\" --pdf-engine=weasyprint --metadata title=\"Anna Robakowska CV\""
      system(cmd)

      if File.exist?(pdf_path)
        FileUtils.mkdir_p(File.dirname(site_pdf_path))
        FileUtils.cp(pdf_path, site_pdf_path)
        Jekyll.logger.info "PDF Generator:", "Successfully updated PDF at http://127.0.0.1:4000/assets/pdf/AnnaRobakowskaCV.pdf"
      end
    ensure
      @pdf_running = false
    end
  end
end
