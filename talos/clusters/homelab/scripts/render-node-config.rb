#!/usr/bin/env ruby
# frozen_string_literal: true

require "yaml"
require "fileutils"

def usage
  warn "Usage: render-node-config.rb BASE_CONFIG OUTPUT_CONFIG PATCH [PATCH ...]"
  warn "Example: scripts/render-node-config.rb generated/controlplane.yaml /private/tmp/cp-03.yaml patches/cluster-api-vip-san.yaml patches/controlplane-cp-03.yaml"
  exit 2
end

def load_docs(path)
  YAML.load_stream(File.read(path)).compact
end

def deep_merge!(target, source)
  source.each do |key, value|
    if target[key].is_a?(Hash) && value.is_a?(Hash)
      deep_merge!(target[key], value)
    else
      target[key] = value
    end
  end
  target
end

base_path, output_path, *patch_paths = ARGV
usage unless base_path && output_path && !patch_paths.empty?

docs = load_docs(base_path)
patch_docs = patch_paths.flat_map { |path| load_docs(path) }

config = docs.first
abort "Base config must start with a Talos machine config document" unless config.is_a?(Hash)

patch_docs.each do |patch|
  next unless patch.is_a?(Hash)

  if patch.key?("machine")
    machine_patch = patch.fetch("machine")
    machine = (config["machine"] ||= {})

    if machine_patch.key?("network")
      network_patch = machine_patch.fetch("network")
      network = (machine["network"] ||= {})
      network["interfaces"] = network_patch["interfaces"] if network_patch.key?("interfaces")
      network["nameservers"] = network_patch["nameservers"] if network_patch.key?("nameservers")

      remainder = network_patch.reject { |key, _| %w[interfaces nameservers].include?(key) }
      deep_merge!(network, remainder)
    end

    remainder = machine_patch.reject { |key, _| key == "network" }
    deep_merge!(machine, remainder)
  elsif patch.key?("cluster")
    cluster = (config["cluster"] ||= {})
    deep_merge!(cluster, patch.fetch("cluster"))
  elsif patch["kind"] == "HostnameConfig"
    patch["auto"] = "off" if patch["auto"] == false
    index = docs.find_index { |doc| doc.is_a?(Hash) && doc["kind"] == "HostnameConfig" }
    index ? docs[index] = patch : docs << patch
  else
    docs << patch
  end
end

FileUtils.mkdir_p(File.dirname(output_path))
File.write(output_path, YAML.dump_stream(*docs))
warn "Rendered #{output_path}"
warn "Output contains Talos secrets. Do not commit or print it."
