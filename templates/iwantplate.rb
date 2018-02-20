require "erb"
require "optparse"
require "ostruct"
require "yaml"


ffmpeg_versions=["3.4.2", "3.3.6", "3.2.10", "3.1.11", "3.0.10", "2.8.14"]
variants = ["ubuntu","debian","centos"]
dependencies = "config.yml"

cwd=File.dirname(__FILE__)
global_config = YAML.load_file(File.join(cwd, dependencies))

deps = global_config["libraries"]
options = OpenStruct.new
options.variant = variants[0]
options.ffmpeg_version = ffmpeg_versions[0]
options.minimal = false
options.list_versions = false
options.list_variants = false
OptionParser.new do |opt|
    opt.on("-m",
           "--minimal",
           "Generate a FROM scratch Dockerfile") do |o|
        options[:minimal] = true
    end
    opt.on("-V",
           "--variant VARIANT",
           "Set the base docker image (#{variants.join('|')}) (default: \"#{options.variant}\")") do |o|
               options[:variant] = o if variants.include? o
           end
    opt.on("-v", 
           "--ffmpeg VERSION",
           "Set the FFmpeg version (default: \"#{options.ffmpeg_version}\")") do |o|
               options[:ffmpeg_version] = o
           end
    opt.on("-l",
           "--list-versions",
          "List the currently supported version") do |o|
               options[:list_versions] = o
           end
    opt.on("-L",
           "--list-variants",
          "List the currently supported variants") do |o|
               options[:list_variants] = o
           end
	deps.each do |libname, config| 
		options[libname] = true
		opt.on("--[no-]#{libname}",
			   "Disable #{libname} (default: enabled)") do |o|
			options[libname] = o
		end
		opt.on("--#{libname}-version LIBVERSION", 
			   "Version to use for #{libname} (default: \"#{config["versions"].keys[0]}\")") do |o|
			if ! config["versions"].keys.include? o
				raise "No #{o} version found for #{libname}" 
			else
				options["#{libname}_version"] = o
			end
		end
	end
end.parse!

if options.list_versions
    puts ffmpeg_versions
    exit(0)
end

if options.list_variants
    puts variants 
    exit(0)
end

if ! options.variant.include? ":" 
    semver = /[^0-9]*([0-9]*)[.]([0-9]*)[.]([0-9]*)([0-9A-Za-z-]*)/.match(options.ffmpeg_version.to_s)
    options.variant += ':' + global_config['ffmpeg']["#{semver[1]}.#{semver[2]}"][options.variant]
end

options.to_h.each do | libname, value |
	unless deps[libname.to_s].nil?
		if options["#{libname}_version"] == nil 
			selected_version = nil
			deps[libname.to_s]["versions"].each do |version, version_conf |
				if !version_conf.nil? and !version_conf["blacklist"].nil? 
					if version_conf["blacklist"]["variants"].nil? or 
						!version_conf["blacklist"]["variants"].include? options.variant
						selected_version = version
					end
				else
					selected_version = version if selected_version.nil?
				end
			end
			options["#{libname}_version"] = selected_version
		end 
		if ! deps[libname.to_s]["versions"][options["#{libname}_version"]].nil?	
			deps[libname.to_s]["versions"][options["#{libname}_version"]].each do | param, val |
				if param =~ /sum/
					options["#{libname}_#{param}"] = val 
				end
			end
		end
	end
end

dockerfile_template = File.new(File.join(cwd, "Dockerfile.erb")).read()

renderer = ERB.new(dockerfile_template)
puts output = renderer.result()

